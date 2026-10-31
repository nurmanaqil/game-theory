import sys, os, json, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / '.tools'))
sys.stdout.reconfigure(encoding='utf-8')
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
from faster_whisper import WhisperModel
import av
_av_open = av.open
def compatible_open(*args, **kwargs):
    kwargs.pop('metadata_errors', None)
    return _av_open(*args, **kwargs)
av.open = compatible_open
source = Path('C:/Penyimpanan Utama/Downloads/WhatsApp Audio 2026-10-20 at 17.39.49.mp4')
with av.open(str(source)) as container:
    print('DURATION_SECONDS', container.duration / 1000000 if container.duration else None, flush=True)
model_dir = ROOT / '.models' / 'whisper-small'
if '--download' in sys.argv:
    from huggingface_hub import snapshot_download
    snapshot_download('Systran/faster-whisper-small', local_dir=str(model_dir), allow_patterns=['config.json','model.bin','tokenizer.json','vocabulary.*','preprocessor_config.json'])
    print('MODEL_READY', flush=True)
    sys.exit(0)
model = WhisperModel(str(model_dir), device='cpu', compute_type='int8', cpu_threads=8)
segments, info = model.transcribe(str(source), language='id', beam_size=5, vad_filter=True, condition_on_previous_text=False)
records=[]
def stamp(t):
    return f'{int(t)//60:02d}:{int(t)%60:02d}'
out=ROOT/'research_notes'/'briefing_transcript_auto.txt'
with out.open('w',encoding='utf-8') as f:
    f.write('Transkripsi otomatis bahasa Indonesia; perlu verifikasi bagian ambigu.\n')
    for s in segments:
        line=f'[{stamp(s.start)} - {stamp(s.end)}] {s.text.strip()}'
        f.write(line+'\n'); f.flush()
        records.append({'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,'no_speech_prob':s.no_speech_prob})
        print(line,flush=True)
(ROOT/'research_notes'/'briefing_segments.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('TRANSCRIPTION_COMPLETE',flush=True)
