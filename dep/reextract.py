"""Re-extract with comma-tail logic layered on top of the full original extract_answer.

Strategy: call original extract_answer (methods 1-7 intact). If it returned
method="last_letter" (the fallback), additionally check if the response tail
has a comma-separated letter pattern. If yes, override to multi-answer.
"""
import json, glob, re, sys
sys.path.insert(0, '.')
from mapspatial.eval.answer import extract_answer, is_correct, _strip_think

VALID_SET = {"A", "B", "C", "D"}


def extract_answer_new(response, sample_meta=None):
    r = extract_answer(response, sample_meta=sample_meta, allow_multi=True)
    # Only intervene on the last_letter fallback
    if r.method == "last_letter" and response:
        clean = _strip_think(response.strip())
        tail = clean[-80:].strip()
        m = re.search(r'([A-D](?:\s*,\s*[A-D])+)', tail)
        if m:
            letters = sorted(set(l.strip().upper() for l in m.group(1).split(",") if l.strip()))
            multi = ",".join(letters)
            if "," in multi:
                return type(r)(answer=multi, method="comma_multi", confident=False)
    return r


if __name__ == "__main__":
    multi_cases = []
    for m in ['InternVL3-8B-Instruct', 'InternVL3_5-8B', 'SenseNova-SI-1.3-Qwen3-VL-8B', 'SenseNova-SI-1.5-InternVL3-8B']:
        old_correct = 0; new_correct = 0; n = 0; changed = 0; multi_count = 0
        for jf in sorted(glob.glob(f'results/{m}/direct/*/*/*/*.jsonl')):
            for line in open(jf):
                d = json.loads(line); n += 1
                pred = d.get('prediction') or ''
                gold = d.get('gold') or ''
                old_em = d.get('exact_match', False)
                if old_em: old_correct += 1
                r = extract_answer_new(pred)
                new_em = is_correct(r.answer, gold)
                if new_em: new_correct += 1
                if old_em != new_em: changed += 1
                if "," in r.answer:
                    multi_count += 1
                    if len(multi_cases) < 80:
                        multi_cases.append({
                            'model': m, 'id': d.get('id', '')[:50],
                            'cell': jf.split(f'{m}/direct/')[1] if f'{m}/direct/' in jf else jf,
                            'gold': gold, 'pred': pred[:120], 'new_extracted': r.answer,
                            'new_method': r.method, 'new_em': new_em,
                            'old_extracted': d.get('extracted_answer', ''),
                            'old_method': d.get('extract_method', ''),
                            'old_em': old_em,
                        })
        print(f"{m:35} n={n} old_acc={old_correct/n:.3f} new_acc={new_correct/n:.3f} changed={changed} multi={multi_count}")

    print(f"\n{'='*80}")
    print(f"Multi-select cases: {len(multi_cases)} shown")
    print(f"{'='*80}")
    for c in multi_cases:
        print(f"\n[{c['model']}] {c['id']}")
        print(f"  cell: {c['cell']}")
        print(f"  gold: {c['gold']!r}")
        print(f"  pred: {c['pred']!r}")
        print(f"  OLD: ext={c['old_extracted']!r} m={c['old_method']} em={c['old_em']}")
        print(f"  NEW: ext={c['new_extracted']!r} m={c['new_method']} em={c['new_em']}")
