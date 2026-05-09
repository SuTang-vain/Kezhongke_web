(function(){
  // Inject nav HTML
  var navHTML = '<nav id="top-nav" class="fixed top-3 inset-x-3 md:top-4 md:inset-x-4 rounded-[28px] border border-white/45 dark:border-white/10 z-[9999] transition-all duration-500 overflow-visible" style="view-transition-name: top-nav;">'
  + '<div class="relative z-10 flex justify-between items-center w-full max-w-[1880px] mx-auto px-5 sm:px-7 lg:px-9 xl:px-11 h-[70px] lg:h-[74px]">'
  + '<a href="/" class="flex items-center leading-none shrink-0 min-w-[150px] lg:min-w-[160px]">'
  + '<span class="text-[24px] sm:text-[26px] font-bold text-orange-600 dark:text-orange-500 font-[Source_Han_Serif_SC,serif] leading-none tracking-normal">Kezhongke</span>'
  + '</a>'
  + '<div class="hidden lg:flex items-center justify-center gap-6 xl:gap-8 2xl:gap-10">'
  + '<a class="nav-link flex h-[56px] items-center gap-1.5 px-1 text-[15px] xl:text-base font-[Inter,sans-serif] transition-colors duration-300" href="/"><span class="font-semibold">首页</span><span class="nav-link-en font-medium">Home</span></a>'
  + '<a class="nav-link flex h-[56px] items-center gap-1.5 px-1 text-[15px] xl:text-base font-[Inter,sans-serif] transition-colors duration-300" href="/grow"><span class="font-semibold">成长</span><span class="nav-link-en font-medium">Grow</span></a>'
  + '<a class="nav-link flex h-[56px] items-center gap-1.5 px-1 text-[15px] xl:text-base font-[Inter,sans-serif] transition-colors duration-300" href="/path"><span class="font-semibold">路径</span><span class="nav-link-en font-medium">Path</span></a>'
  + '<a class="nav-link flex h-[56px] items-center gap-1.5 px-1 text-[15px] xl:text-base font-[Inter,sans-serif] transition-colors duration-300" href="/atelier"><span class="font-semibold">工坊</span><span class="nav-link-en font-medium">Atelier</span></a>'
  + '<a class="nav-link flex h-[56px] items-center gap-1.5 px-1 text-[15px] xl:text-base font-[Inter,sans-serif] transition-colors duration-300" href="/journal"><span class="font-semibold">期刊</span><span class="nav-link-en font-medium">Journal</span></a>'
  + '<a class="nav-link flex h-[56px] items-center gap-1.5 px-1 text-[15px] xl:text-base font-[Inter,sans-serif] transition-colors duration-300" href="/about"><span class="font-semibold">关于</span><span class="nav-link-en font-medium">About</span></a>'
  + '</div>'
  + '<div class="flex items-center gap-3 lg:gap-3 xl:gap-4 shrink-0">'
  + '<label id="search-wrap" class="nav-search hidden xl:flex items-center gap-2 rounded-full h-11 w-[190px] 2xl:w-[220px] px-4 text-orange-600 transition-all duration-300">'
  + '<span class="search-glyph shrink-0" aria-hidden="true"></span>'
  + '<input id="search-input" type="search" placeholder="搜索页面或内容" class="min-w-0 flex-1 bg-transparent outline-none text-[13px] text-on-background placeholder:text-on-surface-variant/48 font-[Inter,sans-serif]" autocomplete="off"/>'
  + '</label>'
  + '<div id="auth-state" class="flex items-center">'
  + '<a href="/auth" id="connect-btn" class="nav-cta flex items-center gap-1.5 rounded-full px-5 lg:px-6 h-11 lg:h-12 text-white font-[Inter,sans-serif] text-xs lg:text-[13px] font-semibold transition-all duration-300 hover:scale-[1.03] active:scale-[0.98]">'
  + '<span>即刻连接</span><span class="font-semibold">Connect</span>'
  + '</a>'
  + '<div id="user-profile" class="hidden relative group">'
  + '<div class="flex items-center gap-3 px-2 py-1 rounded-full hover:bg-white/20 transition-all duration-300 cursor-pointer">'
  + '<div class="w-9 h-9 lg:w-10 lg:h-10 rounded-full bg-primary-container overflow-hidden border-2 border-white/50 shadow-sm">'
  + '<img id="user-avatar" src="/kezhongke_logo/kezhongke_logo.png" class="w-full h-full object-cover" alt="avatar" />'
  + '</div>'
  + '<span id="user-nickname" class="hidden sm:inline font-semibold text-sm text-on-background">用户</span>'
  + '<span class="material-symbols-outlined text-[18px] opacity-40">expand_more</span>'
  + '</div>'
  + '<div class="user-dropdown absolute right-0 mt-2 w-56 py-3 rounded-[24px] overflow-hidden">'
  + '<div class="px-5 py-2 mb-2">'
  + '<p id="user-email-display" class="text-[11px] font-label-caps text-on-surface-variant opacity-60 tracking-wider mb-1 uppercase">guest@kezhongke.cn</p>'
  + '<p class="text-xs text-primary font-semibold uppercase tracking-tighter">探索者 · Explorer</p>'
  + '</div>'
  + '<div class="h-px bg-black/5 mx-4 my-1"></div>'
  + '<a href="#" onclick="showProfileEditor()" class="flex items-center gap-3 px-5 py-3 hover:bg-primary/5 transition-colors text-[14px] font-medium">'
  + '<span class="material-symbols-outlined text-[20px] opacity-60">account_circle</span>'
  + '<span>个人资料</span>'
  + '</a>'
  + '<a href="#" class="flex items-center gap-3 px-5 py-3 hover:bg-primary/5 transition-colors text-[14px] font-medium">'
  + '<span class="material-symbols-outlined text-[20px] opacity-60">history</span>'
  + '<span>成长记录</span>'
  + '</a>'
  + '<div class="h-px bg-black/5 mx-4 my-1"></div>'
  + '<button onclick="handleLogout()" class="w-full flex items-center gap-3 px-5 py-3 hover:bg-red-50 text-red-600 transition-colors text-[14px] font-bold">'
  + '<span class="material-symbols-outlined text-[20px]">logout</span>'
  + '<span>登出</span>'
  + '</button>'
  + '</div>'
  + '</div>'
  + '</div>'
  + '</div>'
  + '</div>'
  + '</nav>'
  // Profile editor modal
  + '<div id="profile-modal" style="display:none;" class="fixed inset-0 z-[10001] flex items-center justify-center bg-black/20 backdrop-blur-sm">'
  + '<div class="liquid-glass rounded-3xl p-8 w-full max-w-sm mx-4 space-y-6">'
  + '<div class="flex justify-between items-center">'
  + '<h3 class="text-lg font-bold text-on-background">编辑个人资料</h3>'
  + '<button onclick="hideProfileEditor()" class="text-on-surface-variant hover:text-on-background text-xl">&times;</button>'
  + '</div>'
  + '<div class="space-y-6">'
  + '<div class="space-y-2">'
  + '<label class="text-sm font-semibold px-1 opacity-70">昵称</label>'
  + '<input type="text" id="edit-nickname" class="w-full bg-white/30 border border-white/50 rounded-2xl px-5 py-3 outline-none focus:border-primary/30 transition-all">'
  + '</div>'
  + '<div class="space-y-2">'
  + '<label class="text-sm font-semibold px-1 opacity-70">个人简介</label>'
  + '<textarea id="edit-bio" rows="3" class="w-full bg-white/30 border border-white/50 rounded-2xl px-5 py-3 outline-none focus:border-primary/30 transition-all placeholder:opacity-40" placeholder="写点什么，让大家了解你..."></textarea>'
  + '</div>'
  + '<div id="profile-msg" class="text-xs hidden"></div>'
  + '<div class="flex gap-4 pt-2">'
  + '<button onclick="hideProfileEditor()" class="flex-1 py-3 rounded-2xl bg-black/5 font-semibold">取消</button>'
  + '<button onclick="saveProfile()" id="save-btn" class="flex-1 py-3 rounded-2xl bg-primary text-white font-bold shadow-lg">保存更改</button>'
  + '</div>'
  + '</div>'
  + '</div>'
  + '</div>';

  // Insert at the beginning of body
  var body = document.body;
  var navContainer = document.createElement('div');
  navContainer.innerHTML = navHTML;
  while (navContainer.firstChild) {
    body.insertBefore(navContainer.firstChild, body.firstChild);
  }

  // --- Auth & Profile Logic ---
  function updateAuthState() {
    var token = localStorage.getItem('kezhongke_token');
    var userStr = localStorage.getItem('kezhongke_user');
    var connectBtn = document.getElementById('connect-btn');
    var profileNode = document.getElementById('user-profile');
    if (token && userStr) {
      var user = JSON.parse(userStr);
      connectBtn.classList.add('hidden');
      profileNode.classList.remove('hidden');
      document.getElementById('user-nickname').innerText = user.nickname || '用户';
      document.getElementById('user-email-display').innerText = user.email;
      if (user.avatar_url) document.getElementById('user-avatar').src = user.avatar_url;
    } else {
      connectBtn.classList.remove('hidden');
      profileNode.classList.add('hidden');
    }
  }

  window.handleLogout = function() {
    localStorage.removeItem('kezhongke_token');
    localStorage.removeItem('kezhongke_user');
    window.location.reload();
  };

  window.showProfileEditor = function() {
    var user = JSON.parse(localStorage.getItem('kezhongke_user') || '{}');
    document.getElementById('edit-nickname').value = user.nickname || '';
    document.getElementById('edit-bio').value = user.bio || '';
    document.getElementById('profile-modal').style.display = 'flex';
  };

  window.hideProfileEditor = function() {
    document.getElementById('profile-modal').style.display = 'none';
  };

  window.saveProfile = async function() {
    var btn = document.getElementById('save-btn');
    var msg = document.getElementById('profile-msg');
    var token = localStorage.getItem('kezhongke_token');
    var nickname = document.getElementById('edit-nickname').value;
    var bio = document.getElementById('edit-bio').value;
    btn.disabled = true;
    btn.innerText = '正在保存...';
    try {
      var res = await fetch('/api/auth/me', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token },
        body: JSON.stringify({ nickname: nickname, bio: bio })
      });
      var data = await res.json();
      if (res.ok) {
        localStorage.setItem('kezhongke_user', JSON.stringify(data));
        updateAuthState();
        msg.innerText = '保存成功！';
        msg.className = 'text-xs text-green-600 block';
        setTimeout(hideProfileEditor, 1000);
      } else {
        msg.innerText = data.detail || '保存失败';
        msg.className = 'text-xs text-red-600 block';
      }
    } catch (e) {
      msg.innerText = '网络异常';
      msg.className = 'text-xs text-red-600 block';
    } finally {
      btn.disabled = false;
      btn.innerText = '保存更改';
    }
  };

  updateAuthState();

  var userProfile = document.getElementById('user-profile');
  if (userProfile) {
    var profileTrigger = userProfile.firstElementChild;
    if (profileTrigger) {
      profileTrigger.addEventListener('click', function(e) {
        e.stopPropagation();
        userProfile.classList.toggle('is-open');
      });
    }
    document.addEventListener('click', function(e) {
      if (!userProfile.contains(e.target)) {
        userProfile.classList.remove('is-open');
      }
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        userProfile.classList.remove('is-open');
      }
    });
  }

  // --- Search & Nav Active State ---
  var pages = [
    {name:'首页 Home',href:'/',search:'首页 home'},
    {name:'成长 Grow',href:'/grow',search:'成长 生长 grow'},
    {name:'路径 Path',href:'/path',search:'路径 path'},
    {name:'工坊 Atelier',href:'/atelier',search:'工坊 atelier'},
    {name:'期刊 Journal',href:'/journal',search:'期刊 journal'},
    {name:'关于 About',href:'/about',search:'关于 about'}
  ];
  var p = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(function(a) {
    var h = a.getAttribute('href');
    if (h === p || (h !== '/' && p.startsWith(h))) {
      a.classList.add('is-active');
      a.setAttribute('aria-current', 'page');
    }
  });
  var input = document.getElementById('search-input');
  function firstMatch(q) {
    q = (q || '').toLowerCase().trim();
    if (!q) return null;
    return pages.filter(function(pg) { return pg.search.indexOf(q) > -1 || pg.name.toLowerCase().indexOf(q) > -1; })[0] || null;
  }
  window.toggleSearch = function() { if (input) input.focus(); };
  if (input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') { var match = firstMatch(input.value); if (match) window.location.href = match.href; }
      if (e.key === 'Escape') { input.value = ''; input.blur(); }
    });
  }
})();
