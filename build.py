#!/usr/bin/env python3
"""Build script: reads the original POC and creates the complete sistema."""
import re

# Read original POC
with open("../POC Jurídico Lavvi.html", "r") as f:
    orig = f.read()

# Extract logo base64
logo_match = re.search(r'src="(data:image/png;base64,[^"]+)"', orig)
LOGO = logo_match.group(1) if logo_match else ""

# Extract original CSS (between first <style> and </style> after line 5)
css_match = re.search(r'<style>\s*/\* Identidade.*?</style>', orig, re.DOTALL)
ORIG_CSS = css_match.group(0).replace('<style>', '').replace('</style>', '').strip() if css_match else ""

# Extract original app HTML (from <div class="app"> to its close before <script>)
app_match = re.search(r'(<div class="app">.*?)\s*<script>', orig, re.DOTALL)
ORIG_APP_HTML = app_match.group(1).strip() if app_match else ""

# Extract original JS
js_match = re.search(r'<script>\s*\(function\(\)\{(.*?)\}\)\(\);\s*</script>', orig, re.DOTALL)
ORIG_JS = js_match.group(1).strip() if js_match else ""

# --- BUILD NEW FILE ---

NEW_CSS = """
/* === SCREEN MANAGEMENT === */
html,body{height:100%;margin:0;padding:0;overflow:hidden}
[hidden]{display:none!important}

/* === LOGIN === */
.screen-login{height:100%;display:flex;align-items:center;justify-content:center;background:var(--bg);font-family:var(--font)}
.login-card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:48px 40px;width:100%;max-width:400px;display:flex;flex-direction:column;gap:24px;align-items:center;box-shadow:0 4px 24px rgba(0,0,0,.06);position:relative}
.login-card::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:var(--accent);border-radius:16px 16px 0 0}
.login-card .brand-login{display:flex;align-items:center;gap:12px}
.login-card .brand-login .sep{font-family:var(--display);font-size:22px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-left:12px;border-left:1px solid var(--line);line-height:1}
.login-card .form-group{width:100%;display:flex;flex-direction:column;gap:6px}
.login-card label{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.login-card input{font:inherit;font-size:14px;padding:12px 14px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink);width:100%;box-sizing:border-box}
.login-card input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.login-btn{width:100%;padding:14px;border-radius:8px;border:0;background:var(--navy);color:#fff;font:inherit;font-weight:600;font-size:14px;cursor:pointer;letter-spacing:.02em;min-height:48px}
.login-btn:hover{background:var(--navy-2)}
.login-error{color:var(--bad);font-size:12px;text-align:center;min-height:18px}
.login-hint{font-size:11px;color:var(--muted);text-align:center}

/* === USERS === */
.screen-users{height:100%;display:flex;flex-direction:column;overflow:hidden;font-family:var(--font);background:var(--bg);color:var(--ink)}
.users-top{background:var(--surface);border-bottom:1px solid var(--line);padding:14px 24px;display:flex;align-items:center;justify-content:space-between;gap:12px;position:relative}
.users-top::before{content:"";position:absolute;left:0;right:0;top:0;height:3px;background:var(--accent)}
.users-body{flex:1;overflow-y:auto;padding:24px}
.users-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px}
.users-header h2{font-family:var(--display);font-size:22px;font-weight:600;margin:0}
.users-table{width:100%;border-collapse:separate;border-spacing:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.users-table th{text-align:left;padding:12px 16px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);background:var(--side);border-bottom:1px solid var(--line)}
.users-table td{padding:14px 16px;border-bottom:1px solid var(--line);font-size:13px}
.users-table tr:last-child td{border-bottom:0}
.users-table .role-pill{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:600}
.role-admin{background:var(--soft);color:var(--soft-ink)}
.role-advogado{background:var(--info-bg);color:var(--info)}
.role-coordenador{background:var(--ok-bg);color:var(--ok)}
.status-ativo{color:var(--ok);font-weight:500}
.status-inativo{color:var(--muted)}
.users-table .actions{display:flex;gap:6px}
.users-table .actions button{padding:6px 12px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink);font-size:12px;cursor:pointer;font-family:inherit;min-height:32px}
.users-table .actions button:hover{background:var(--bg)}
.users-table .actions .btn-del{color:var(--bad);border-color:var(--bad-line)}
.users-table .actions .btn-del:hover{background:var(--bad-bg)}
.btn-add-user{padding:10px 20px;border-radius:8px;border:0;background:var(--navy);color:#fff;font:inherit;font-weight:600;cursor:pointer;min-height:40px}
.btn-add-user:hover{background:var(--navy-2)}

/* === MODAL === */
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;z-index:999}
.modal-card{background:var(--surface);border-radius:12px;padding:32px;width:100%;max-width:440px;display:flex;flex-direction:column;gap:20px;box-shadow:0 8px 32px rgba(0,0,0,.12)}
.modal-card h3{font-family:var(--display);font-size:20px;font-weight:600;margin:0}
.modal-card .form-group{display:flex;flex-direction:column;gap:6px}
.modal-card label{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.modal-card input,.modal-card select{font:inherit;font-size:14px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--ink)}
.modal-card input:focus,.modal-card select:focus{outline:2px solid var(--accent);outline-offset:1px}
.modal-actions{display:flex;gap:8px;justify-content:flex-end}
.modal-actions button{padding:10px 20px;border-radius:8px;font:inherit;font-weight:500;cursor:pointer;min-height:40px}
.modal-actions .btn-cancel{border:1px solid var(--line);background:var(--surface);color:var(--ink)}
.modal-actions .btn-save{border:0;background:var(--navy);color:#fff}
.modal-actions .btn-save:hover{background:var(--navy-2)}

/* === NAV LINKS === */
.nav-links{display:flex;align-items:center;gap:8px}
.nav-links button{padding:5px 12px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--ink);font:inherit;font-size:12px;cursor:pointer;min-height:32px}
.nav-links button:hover{background:var(--bg)}
.nav-links .btn-logout{color:var(--bad);border-color:var(--bad-line)}
.nav-links .btn-logout:hover{background:var(--bad-bg)}
.nav-links .who{color:var(--muted);font-size:12px}

/* === NO-SCROLL FIX FOR MAIN APP === */
.app{height:100%;overflow:hidden}
.shell{overflow:hidden}
.pane{min-height:0}
.side{overflow:hidden}
.side .list{overflow-y:auto;flex:1;min-height:0}
.chat{overflow:hidden}
.chat .msgs{overflow-y:auto;flex:1;min-height:0}
.doc{overflow-y:auto}

@media(max-width:600px){
  .login-card{padding:32px 24px;margin:16px}
  .users-body{padding:16px}
  .users-table{font-size:12px}
  .users-table th,.users-table td{padding:10px 12px}
}
"""

# Modify the original app HTML to add id, hidden, and nav buttons
MODIFIED_APP = ORIG_APP_HTML.replace(
    '<div class="app">',
    '<div class="app" id="screen-app" hidden>'
).replace(
    '<span class="who">Dra. Mariana F.</span>',
    '<span class="who" id="app-who">Dra. Mariana F.</span>'
).replace(
    '    <button class="menu" id="menu"',
    '    <button class="nav-links" onclick="showScreen(\'users\')" style="padding:5px 11px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--ink);font-size:12px;cursor:pointer">Usu\\u00e1rios</button>\n    <button class="nav-links btn-logout" onclick="doLogout()" style="padding:5px 11px;border-radius:999px;border:1px solid var(--bad-line);background:transparent;color:var(--bad);font-size:12px;cursor:pointer">Sair</button>\n    <button class="menu" id="menu"'
)

# Fix the unicode escape
MODIFIED_APP = MODIFIED_APP.replace('Usu\\u00e1rios', 'Usuários')

LOGIN_HTML = f'''
<div id="screen-login" class="screen-login">
  <div class="login-card">
    <div class="brand-login">
      <img src="{LOGO}" alt="Lavvi" style="height:30px">
      <span class="sep">Jurídico</span>
    </div>
    <div class="form-group">
      <label for="login-email">E-mail</label>
      <input type="email" id="login-email" placeholder="seu@email.com.br" value="mariana@lavvi.com.br">
    </div>
    <div class="form-group">
      <label for="login-pass">Senha</label>
      <input type="password" id="login-pass" placeholder="••••••" value="123456">
    </div>
    <div class="login-error" id="login-error"></div>
    <button class="login-btn" id="login-btn">Entrar</button>
    <span class="login-hint">Sistema mockado · qualquer senha funciona</span>
  </div>
</div>
'''

USERS_HTML = f'''
<div id="screen-users" class="screen-users" hidden>
  <div class="users-top">
    <div style="display:flex;align-items:center;gap:12px">
      <img src="{LOGO}" alt="Lavvi" style="height:26px">
      <span style="font-family:var(--display);font-size:20px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:var(--accent);padding-left:12px;border-left:1px solid var(--line);line-height:1">Jurídico</span>
    </div>
    <div class="nav-links">
      <span class="who" id="users-who"></span>
      <button onclick="showScreen('app')">Voltar ao sistema</button>
      <button class="btn-logout" onclick="doLogout()">Sair</button>
    </div>
  </div>
  <div class="users-body">
    <div class="users-header">
      <h2>Gerenciamento de Usuários</h2>
      <button class="btn-add-user" onclick="openUserModal()">+ Novo Usuário</button>
    </div>
    <table class="users-table">
      <thead>
        <tr><th>Nome</th><th>E-mail</th><th>Cargo</th><th>Status</th><th>Ações</th></tr>
      </thead>
      <tbody id="users-tbody"></tbody>
    </table>
  </div>
</div>
'''

MODAL_HTML = '''
<div id="modal-user" class="modal-overlay" hidden>
  <div class="modal-card">
    <h3 id="modal-title">Novo Usuário</h3>
    <div class="form-group">
      <label for="user-name">Nome</label>
      <input type="text" id="user-name" placeholder="Nome completo">
    </div>
    <div class="form-group">
      <label for="user-email">E-mail</label>
      <input type="email" id="user-email" placeholder="email@lavvi.com.br">
    </div>
    <div class="form-group">
      <label for="user-role">Cargo</label>
      <select id="user-role">
        <option value="Administrador">Administrador</option>
        <option value="Advogado(a)">Advogado(a)</option>
        <option value="Coordenador(a)">Coordenador(a)</option>
      </select>
    </div>
    <div class="form-group">
      <label for="user-status">Status</label>
      <select id="user-status">
        <option value="Ativo">Ativo</option>
        <option value="Inativo">Inativo</option>
      </select>
    </div>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeUserModal()">Cancelar</button>
      <button class="btn-save" onclick="saveUser()">Salvar</button>
    </div>
  </div>
</div>
'''

JS_CODE = '''
(function(){
  /* ========== MOCK DATA ========== */
  var users = [
    {id:1, name:'Dra. Mariana Ferreira', email:'mariana@lavvi.com.br', role:'Advogado(a)', status:'Ativo'},
    {id:2, name:'Dr. Rafael Campos', email:'rafael@lavvi.com.br', role:'Coordenador(a)', status:'Ativo'},
    {id:3, name:'Ana Souza', email:'ana@lavvi.com.br', role:'Administrador', status:'Ativo'},
    {id:4, name:'Carlos Lima', email:'carlos@lavvi.com.br', role:'Advogado(a)', status:'Inativo'}
  ];
  var nextId = 5, editingId = null, currentUser = null;

  /* ========== SCREEN MANAGEMENT ========== */
  window.showScreen = function(name){
    document.getElementById('screen-login').hidden = (name !== 'login');
    document.getElementById('screen-users').hidden = (name !== 'users');
    document.getElementById('screen-app').hidden = (name !== 'app');
    if(name === 'users'){ renderUsers(); }
    if(name === 'users' && currentUser) document.getElementById('users-who').textContent = currentUser.name;
    if(name === 'app' && currentUser){
      var w = document.getElementById('app-who');
      if(w) w.textContent = currentUser.name;
    }
  };

  /* ========== LOGIN ========== */
  function doLogin(){
    var email = document.getElementById('login-email').value.trim();
    if(!email){ document.getElementById('login-error').textContent = 'Informe o e-mail'; return; }
    var user = users.find(function(u){ return u.email === email; });
    if(!user) user = {name: email.split('@')[0], email: email, role:'Advogado(a)'};
    currentUser = user;
    try{ localStorage.setItem('lavvi-user', JSON.stringify(user)); }catch(e){}
    document.getElementById('login-error').textContent = '';
    showScreen('app');
  }
  document.getElementById('login-btn').addEventListener('click', doLogin);
  document.getElementById('login-pass').addEventListener('keydown', function(e){ if(e.key==='Enter') doLogin(); });
  document.getElementById('login-email').addEventListener('keydown', function(e){ if(e.key==='Enter') document.getElementById('login-pass').focus(); });

  window.doLogout = function(){
    currentUser = null;
    try{ localStorage.removeItem('lavvi-user'); }catch(e){}
    document.getElementById('login-error').textContent = '';
    showScreen('login');
  };

  /* ========== USER MANAGEMENT ========== */
  function renderUsers(){
    var tbody = document.getElementById('users-tbody');
    tbody.innerHTML = '';
    users.forEach(function(u){
      var rc = u.role === 'Administrador' ? 'role-admin' : (u.role.indexOf('Advogado') >= 0 ? 'role-advogado' : 'role-coordenador');
      var sc = u.status === 'Ativo' ? 'status-ativo' : 'status-inativo';
      var tr = document.createElement('tr');
      tr.innerHTML = '<td><strong>' + u.name + '</strong></td>' +
        '<td>' + u.email + '</td>' +
        '<td><span class="role-pill ' + rc + '">' + u.role + '</span></td>' +
        '<td class="' + sc + '">' + u.status + '</td>' +
        '<td class="actions"><button onclick="editUser(' + u.id + ')">Editar</button><button class="btn-del" onclick="deleteUser(' + u.id + ')">Excluir</button></td>';
      tbody.appendChild(tr);
    });
  }
  window.openUserModal = function(id){
    editingId = id || null;
    document.getElementById('modal-title').textContent = id ? 'Editar Usuário' : 'Novo Usuário';
    if(id){
      var u = users.find(function(x){ return x.id === id; });
      if(u){
        document.getElementById('user-name').value = u.name;
        document.getElementById('user-email').value = u.email;
        document.getElementById('user-role').value = u.role;
        document.getElementById('user-status').value = u.status;
      }
    } else {
      document.getElementById('user-name').value = '';
      document.getElementById('user-email').value = '';
      document.getElementById('user-role').value = 'Advogado(a)';
      document.getElementById('user-status').value = 'Ativo';
    }
    document.getElementById('modal-user').hidden = false;
  };
  window.closeUserModal = function(){ document.getElementById('modal-user').hidden = true; editingId = null; };
  window.saveUser = function(){
    var name = document.getElementById('user-name').value.trim();
    var email = document.getElementById('user-email').value.trim();
    var role = document.getElementById('user-role').value;
    var status = document.getElementById('user-status').value;
    if(!name || !email) return;
    if(editingId){
      var u = users.find(function(x){ return x.id === editingId; });
      if(u){ u.name=name; u.email=email; u.role=role; u.status=status; }
    } else {
      users.push({id:nextId++, name:name, email:email, role:role, status:status});
    }
    closeUserModal();
    renderUsers();
  };
  window.editUser = function(id){ openUserModal(id); };
  window.deleteUser = function(id){
    if(!confirm('Excluir este usuário?')) return;
    users = users.filter(function(u){ return u.id !== id; });
    renderUsers();
  };
  // Close modal on overlay click
  document.getElementById('modal-user').addEventListener('click', function(e){ if(e.target === this) closeUserModal(); });

  /* ========== ORIGINAL POC LOGIC (case switching) ========== */
  ''' + ORIG_JS + '''

  /* ========== INIT ========== */
  var stored = null;
  try{ stored = localStorage.getItem('lavvi-user'); }catch(e){}
  if(stored){
    try{ currentUser = JSON.parse(stored); showScreen('app'); }catch(e){ showScreen('login'); }
  } else {
    showScreen('login');
  }
})();
'''

# Assemble final HTML
FINAL = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Lavvi Jurídico · Sistema</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&family=Cormorant+Garamond:wght@500;600&family=Source+Serif+4:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
{ORIG_CSS}
{NEW_CSS}
</style>
</head>
<body>

{LOGIN_HTML}

{USERS_HTML}

{MODIFIED_APP}

{MODAL_HTML}

<script>
{JS_CODE}
</script>

</body>
</html>'''

# Write output
with open("index.html", "w") as f:
    f.write(FINAL)

print(f"OK - wrote index.html ({len(FINAL)} chars, ~{FINAL.count(chr(10))} lines)")
