# -*- coding: utf-8 -*-
import os
import sys
import random
import pandas as pd
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, jsonify, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STIMULI_DIR = os.path.join(BASE_DIR, 'stimuli')
DATA_DIR = os.path.join(BASE_DIR, 'data')

app = Flask(__name__, template_folder=BASE_DIR)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def index():
    return render_template('web_experiment.html')

@app.route('/stimuli/<path:filename>')
def serve_stimuli(filename):
    return send_from_directory(STIMULI_DIR, filename)

@app.route('/init_data', methods=['POST'])
def init_data():
    """根据 Session ID 生成实验试次数据"""
    data = request.json
    session_id = data.get('session', '1')

    session_trials = []
    radical_trials = []

    def get_stim_url(subfolder, cond, num, ext):
        padded = f"{cond}_{num:02d}{ext}"
        unpadded = f"{cond}_{num}{ext}"
        
        full_path_padded = os.path.join(STIMULI_DIR, subfolder, padded)
        if os.path.exists(full_path_padded):
            return f"/stimuli/{subfolder}/{padded}"
            
        return f"/stimuli/{subfolder}/{unpadded}"

    if session_id == 'radical':
        form_trials = []
        for i in range(1, 6):
            img_A = f"/stimuli/radical_awareness/form_reg_A_{i}.png"
            img_B = f"/stimuli/radical_awareness/form_reg_B_{i}.png"
            
            if random.random() > 0.5:
                left_img, right_img = img_B, img_A
                left_char, right_char = 'B', 'A'
            else:
                left_img, right_img = img_A, img_B
                left_char, right_char = 'A', 'B'

            form_trials.append({
                'type': 'form',
                'left_image': left_img,
                'right_image': right_img,
                'left_char': left_char,
                'right_char': right_char,
                'correct_answer': 'A' 
            })
            
        pos_trials = []
        for i in range(1, 6):
            img_A = f"/stimuli/radical_awareness/pos_reg_A_{i}.png"
            img_B = f"/stimuli/radical_awareness/pos_reg_B_{i}.png"
            
            if random.random() > 0.5:
                left_img, right_img = img_B, img_A
                left_char, right_char = 'B', 'A'
            else:
                left_img, right_img = img_A, img_B
                left_char, right_char = 'A', 'B'
                
            pos_trials.append({
                'type': 'pos',
                'left_image': left_img,
                'right_image': right_img,
                'left_char': left_char,
                'right_char': right_char,
                'correct_answer': 'A'
            })
        
        radical_trials = form_trials + pos_trials
        random.shuffle(radical_trials)
    else:
        try:
            session_num = int(session_id)
        except (ValueError, TypeError):
            session_num = 1
        
        excel_path = os.path.join(STIMULI_DIR, 'definitions.xlsx')
        if not os.path.exists(excel_path):
            return jsonify({'error': '找不到 definitions.xlsx 文件'}), 404
        
        df = pd.read_excel(excel_path)
        
        conditions = ['FS_R', 'FS_NR', 'MS_R', 'MS_NR']
        items_per_session = 3
        start_index = (session_num - 1) * items_per_session
        
        for cond in conditions:
            for i in range(start_index, start_index + items_per_session):
                item_num = i + 1
                try:
                    definition = df.loc[i, cond]
                    if pd.isna(definition):
                        definition = "定义缺失"
                    else:
                        definition = str(definition)
                except (IndexError, KeyError):
                    definition = "定义缺失"

                trial = {
                    'id': f'{cond}_{item_num:02d}',
                    'condition': cond,
                    'image': get_stim_url('images', cond, item_num, '.png'),
                    'meaning': get_stim_url('meanings', cond, item_num, '.png'),
                    'audio': get_stim_url('pronunciations', cond, item_num, '.wav'),
                    'definition': definition
                }
                session_trials.append(trial)
                
        random.shuffle(session_trials)

    return jsonify({
        'study_trials': session_trials,
        'radical_trials': radical_trials
    })

@app.route('/save_data', methods=['POST'])
def save_data():
    """保存实验数据到 CSV"""
    req_data = request.json
    csv_data = req_data.get('csv_data')
    filename = req_data.get('filename', 'experiment_data.csv')
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    file_path = os.path.join(DATA_DIR, filename)
    
    with open(file_path, 'w', encoding='utf-8-sig') as f:
        f.write(csv_data)
        
    print(f"数据已保存: {file_path}")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("正在启动实验服务器...")
    print("如果浏览器没有自动打开，请访问: http://127.0.0.1:5000/")
    
    try:
        import flask
        import pandas
        import openpyxl
    except ImportError as e:
        print(f"错误: 缺少必要的库 {e.name}。")
        print("请运行: pip install flask pandas openpyxl")
        sys.exit(1)

    Timer(1, open_browser).start()
    
    app.run(port=5000, debug=True, use_reloader=False)