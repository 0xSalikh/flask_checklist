from flask import Flask, render_template, url_for, request, flash, get_flashed_messages, redirect

app = Flask(__name__)
app.secret_key = "454b7e6f247f8c473f7bab13063e788eddbfb6e3"

class Resume:
    def __init__(self):
        with open('data/resume.txt', 'r') as file:
            self.data = file.readlines()
            
    def get_data(self):
        return self.data
    
    def add_data(self, new_data):
        self.data.append(f'{new_data}\n')
        with open('data/resume.txt', 'w') as file:
            file.writelines(self.data)
            return self.data
            
    def del_data(self, data):
        if f'{data}\n' in self.data:
            self.data.remove(f'{data}\n')
            with open('data/resume.txt', 'w') as file:
                file.writelines(self.data)
            return data
        else:
            print('some error')
            return None


@app.route('/', methods=['GET', 'POST'])
def index():
    resume = Resume()
    messages = get_flashed_messages()
    if request.method == 'GET':
        return render_template(
            'index.html',
            resume=resume.get_data(),
            info = messages,
            )
    if request.method == 'POST':
        return render_template(
            'index.html',
            resume=resume.get_data(),
            info = messages,
            ), 302



@app.route('/admin_panel')
def admin():
    return render_template('admin/admin_menu.html')


@app.post('/admin_panel/actions/')
def admin_actions():
    action = request.args.get('action')
    if action == 'del_string':
        data_from_form=request.form.to_dict()
        resume = Resume()
        del_res = resume.del_data(data_from_form['text'])
        if del_res is None:
            return render_template(
            'admin/admin_menu.html',
            error = 'No such string',
            text=data_from_form['text'],
            all_data = resume.get_data()
            )
        flash('Удаление прошло успешно')
        return redirect('/')
    if action == 'add_string':
        data_from_form=request.form.to_dict()
        resume = Resume()
        resume.add_data(data_from_form['text'])
        return redirect('/')
        
    return redirect('/')
