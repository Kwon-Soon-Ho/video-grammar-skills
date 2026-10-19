from pathlib import Path
import sys,json,copy,hashlib
HERE=Path(__file__).resolve().parent
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def write(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def check(reg,matrix,regression,verify_files=True):
    errors=[];required={s['id'] for s in reg['subjects']};byid={s['id']:s for s in matrix['rows']}
    if len(byid)!=len(matrix['rows']):errors.append('duplicate_row')
    if set(byid)!=required:errors.append('missing_or_extra_subject')
    for id,row in byid.items():
        if set(row.get('axis_checks',{}))!=set(reg['required_axes']):errors.append('missing_axis:'+id)
        if any(not isinstance(v,str) or len(v.strip())<8 for v in row.get('axis_checks',{}).values()):errors.append('empty_or_unexplained_axis:'+id)
        if not row.get('evidence'):errors.append('missing_evidence:'+id)
        if not row.get('review_state') or not row.get('reviewer'):errors.append('missing_review_state:'+id)
        if row['prior_relation'] in ['신규 누락 발견','추가 세분화','N4 세분화'] and row['human_approval_scope']!='AI_new_observation_not_human_approved':errors.append('unearned_human_approval:'+id)
        if verify_files:
            for p in row.get('evidence',[]):
                path=Path(p['path'])
                if not path.is_file() or sha(path)!=p['sha256']:errors.append('bad_evidence_pin:'+id)
    for case in regression['cases']:
        for id in case['required_ids']:
            if id not in byid:errors.append('past_omission_not_covered:'+id)
    for id in ['E-outline-light','E-cursor','E-selection','E-connector','E-ui1-row','E-ui1-thumb']:
        if id in byid and not any(p.get('basis','').startswith('native 3840') for p in byid[id]['evidence']):errors.append('critical_native_check_missing:'+id)
    return errors
def main():
    reg=json.loads((HERE/'01_대상목록.json').read_text(encoding='utf-8'));matrix=json.loads((HERE/'02_속성검수표.json').read_text(encoding='utf-8'));regression=json.loads((HERE/'04_회귀확인_과거누락.json').read_text(encoding='utf-8'))
    errors=check(reg,matrix,regression)
    if errors:raise ValueError(errors)
    tests=[]
    for name,edit,needle in [
      ('delete_cursor',lambda m:m.update(rows=[r for r in m['rows'] if r['id']!='E-cursor']),'missing_or_extra_subject'),
      ('delete_new_connector',lambda m:m.update(rows=[r for r in m['rows'] if r['id']!='E-connector']),'missing_or_extra_subject'),
      ('delete_new_UI_internal_state',lambda m:m.update(rows=[r for r in m['rows'] if r['id']!='E-ui1-thumb']),'missing_or_extra_subject'),
      ('blank_curve',lambda m:next(r for r in m['rows'] if r['id']=='E-outline-light')['axis_checks'].update(가감속=''),'empty_or_unexplained_axis:E-outline-light'),
      ('remove_evidence',lambda m:next(r for r in m['rows'] if r['id']=='E-selection').update(evidence=[]),'missing_evidence:E-selection'),
      ('reuse_old_human_approval',lambda m:next(r for r in m['rows'] if r['id']=='E-connector').update(human_approval_scope='prior_scope_only'),'unearned_human_approval:E-connector')]:
        mutant=copy.deepcopy(matrix);edit(mutant);errors=check(reg,mutant,regression,False);assert needle in errors,(name,errors)
        tests.append({'name':name,'expected_failure_detected':True,'errors':errors})
    if '--records-only' in sys.argv:
        result={'structure_gate_passed':True,'subjects':len(reg['subjects']),'axis_cells':len(reg['subjects'])*len(reg['required_axes']),'negative_controls':tests,'source_redecode_performed':False,'scope':'saved records/evidence pins only, no recognition accuracy or omission guarantee'}
        write(HERE/'06_절차검사_재실행.json',result);print(json.dumps({'records_only':True,'passed':True,'subjects':len(reg['subjects']),'negative_controls':len(tests)}));return
    overlap=[];total=0
    for group in ['eg_intro','eg_late','eg_model','jh_all','eg_fine']:
        aid='자료005' if group=='jh_all' else '자료013';run=json.loads((HERE/'cases'/aid/group/'실행기록.json').read_text(encoding='utf-8'))
        assert run['complete_target_selection'] and run['input_sha256']==run['input_sha256_after'] and run['timing_status']=='all_decoded_frame_pts_match_reconstructed_sample_tables_in_this_window'
        for f in run['frames']:assert sha(Path(f['path']))==f['sha256']
        total+=len(run['frames'])
        if group=='eg_fine':
            old=json.loads((HERE.parent/'phase01a-a2-correction2/cases/자료013/detail/실행기록.json').read_text(encoding='utf-8'))
            a={f['actual_playback_seconds']:f for f in old['frames']}
            for f in run['frames']:
                if f['actual_playback_seconds'] in a:
                    prior=a[f['actual_playback_seconds']];assert f['sha256']==prior['sha256']
                    overlap.append({'seconds':f['actual_playback_seconds'],'same_native_PNG':True})
    result={'structure_gate_passed':True,'subjects':len(reg['subjects']),'axis_cells':len(reg['subjects'])*len(reg['required_axes']),'negative_controls':tests,'extracted_PNGs':total,'overlap_native_reproducibility':overlap,'scope':'record consistency and deterministic source-frame integrity only; not recognition accuracy, no omission guarantee, or independent review','A3_started':False}
    write(HERE/'06_절차검사.json',result);print(json.dumps({'subjects':result['subjects'],'axis_cells':result['axis_cells'],'negative_controls_detected':len(tests),'images':total,'native_overlap_matches':len(overlap)},ensure_ascii=False))
if __name__=='__main__':main()
