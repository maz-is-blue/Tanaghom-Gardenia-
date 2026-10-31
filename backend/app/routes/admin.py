import os
import shutil
import subprocess
import time
from collections import defaultdict
from functools import wraps
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for, flash, current_app)
from werkzeug.utils import secure_filename
from ..content import load, save as save_content

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ── helpers ──────────────────────────────────────────────────────────────────

def _upload_dir():
    return os.path.join(current_app.static_folder, 'uploads')

def _project_root():
    return os.path.dirname(os.path.dirname(current_app.root_path))

# In-memory per-process login throttle (fine for the single-worker deployment
# this app runs under; resets on restart).
_LOGIN_MAX_ATTEMPTS  = 5
_LOGIN_WINDOW_SECONDS = 15 * 60
_login_attempts = defaultdict(list)

def _login_rate_limited(key):
    now = time.time()
    attempts = [t for t in _login_attempts[key] if now - t < _LOGIN_WINDOW_SECONDS]
    _login_attempts[key] = attempts
    return len(attempts) >= _LOGIN_MAX_ATTEMPTS

def _record_login_failure(key):
    _login_attempts[key].append(time.time())

ALLOWED_IMG   = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ALLOWED_AUDIO = {'mp3', 'wav', 'ogg', 'm4a', 'aac'}
ALLOWED_VIDEO = {'mp4', 'webm', 'mov', 'avi'}

def _allowed(filename, exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in exts

def _format_date(raw):
    months_en = ['January','February','March','April','May','June',
                 'July','August','September','October','November','December']
    months_ar = ['يناير','فبراير','مارس','أبريل','مايو','يونيو',
                 'يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر']
    if not raw or '-' not in raw:
        return raw, raw
    try:
        y, m = raw.split('-')[:2]
        idx = int(m) - 1
        return '{} {}'.format(months_en[idx], y), '{} {}'.format(months_ar[idx], y)
    except Exception:
        return raw, raw

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated

# ── auth ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        key = request.remote_addr or 'unknown'
        if _login_rate_limited(key):
            flash('Too many failed attempts. Try again in a few minutes.', 'error')
            return render_template('admin/login.html')
        pw = request.form.get('password', '')
        if pw == current_app.config.get('ADMIN_PASSWORD', 'tanaghom2024'):
            session.clear()
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        _record_login_failure(key)
        flash('Wrong password.', 'error')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.login'))

# ── dashboard ────────────────────────────────────────────────────────────────

@admin_bp.route('/')
@login_required
def dashboard():
    gallery = load('gallery', {'items': []})
    audio   = load('audio',   {'tracks': []})
    home    = load('home',    {'events': []})
    return render_template('admin/dashboard.html', active='dashboard',
        gallery_count=len(gallery.get('items', [])),
        audio_count=len(audio.get('tracks', [])),
        event_count=len(home.get('events', [])))

# ── home page ────────────────────────────────────────────────────────────────

@admin_bp.route('/home')
@login_required
def home_page():
    return render_template('admin/home_page.html', active='home',
                           data=load('home', {}))

@admin_bp.route('/home/save-hero', methods=['POST'])
@login_required
def save_hero():
    data = load('home', {})
    data['hero'] = {k: request.form.get(k, '') for k in
                    ('eyebrow_en', 'eyebrow_ar', 'tagline_en', 'tagline_ar')}
    save_content('home', data)
    flash('Hero section saved.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/save-intro', methods=['POST'])
@login_required
def save_intro():
    data = load('home', {})
    data['intro'] = {k: request.form.get(k, '') for k in
                     ('lead_en', 'lead_ar',
                      'story_founding_en', 'story_founding_ar',
                      'story_today_en', 'story_today_ar')}
    save_content('home', data)
    flash('Story saved.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/save-stats', methods=['POST'])
@login_required
def save_home_stats():
    data = load('home', {})
    nums      = request.form.getlist('num')
    formats   = request.form.getlist('format')
    labels_en = request.form.getlist('label_en')
    labels_ar = request.form.getlist('label_ar')
    data['stats'] = [
        {'num': nums[i], 'format': formats[i],
         'label_en': labels_en[i], 'label_ar': labels_ar[i]}
        for i in range(len(nums))
    ]
    save_content('home', data)
    flash('Stats saved.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/event/add', methods=['POST'])
@login_required
def event_add():
    data   = load('home', {})
    events = data.get('events', [])
    new_id = max((e['id'] for e in events), default=0) + 1
    events.append({
        'id': new_id,
        **{k: request.form.get(k, '') for k in
           ('day_en','day_ar','month_en','month_ar',
            'title_en','title_ar','type_en','type_ar',
            'place_en','place_ar','url')}
    })
    data['events'] = events
    save_content('home', data)
    flash('Event added.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/event/edit/<int:eid>', methods=['POST'])
@login_required
def event_edit(eid):
    data = load('home', {})
    for e in data.get('events', []):
        if e['id'] == eid:
            for k in ('day_en','day_ar','month_en','month_ar',
                      'title_en','title_ar','type_en','type_ar',
                      'place_en','place_ar','url'):
                e[k] = request.form.get(k, e.get(k, ''))
            break
    save_content('home', data)
    flash('Event updated.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/event/delete/<int:eid>', methods=['POST'])
@login_required
def event_delete(eid):
    data = load('home', {})
    data['events'] = [e for e in data.get('events', []) if e['id'] != eid]
    save_content('home', data)
    flash('Event deleted.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/hero-video/add', methods=['POST'])
@login_required
def hero_video_add():
    data   = load('home', {})
    videos = data.get('hero_videos', [])
    f = request.files.get('video_file')
    if not f or not f.filename or not _allowed(f.filename, ALLOWED_VIDEO):
        flash('Please choose a valid video file (mp4, webm, mov, avi).', 'error')
        return redirect(url_for('admin.home_page'))
    new_id = max((v['id'] for v in videos), default=0) + 1
    ext    = f.filename.rsplit('.', 1)[1].lower()
    fname  = 'hero_video_{}.{}'.format(new_id, ext)
    dest   = os.path.join(_upload_dir(), 'hero', fname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    f.save(dest)
    try:
        order = int(request.form.get('order', len(videos) + 1))
    except ValueError:
        order = len(videos) + 1
    videos.append({
        'id': new_id,
        'file': '/static/uploads/hero/' + fname,
        'order': order,
        'visible': request.form.get('visible') == 'on',
    })
    data['hero_videos'] = videos
    save_content('home', data)
    flash('Hero video added.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/hero-video/edit/<int:vid>', methods=['POST'])
@login_required
def hero_video_edit(vid):
    data = load('home', {})
    for v in data.get('hero_videos', []):
        if v['id'] == vid:
            try:
                v['order'] = int(request.form.get('order', v.get('order', 0)))
            except ValueError:
                pass
            v['visible'] = request.form.get('visible') == 'on'
            f = request.files.get('video_file')
            if f and f.filename and _allowed(f.filename, ALLOWED_VIDEO):
                ext   = f.filename.rsplit('.', 1)[1].lower()
                fname = 'hero_video_{}.{}'.format(vid, ext)
                dest  = os.path.join(_upload_dir(), 'hero', fname)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                f.save(dest)
                v['file'] = '/static/uploads/hero/' + fname
            break
    save_content('home', data)
    flash('Hero video updated.', 'success')
    return redirect(url_for('admin.home_page'))

@admin_bp.route('/home/hero-video/delete/<int:vid>', methods=['POST'])
@login_required
def hero_video_delete(vid):
    data = load('home', {})
    data['hero_videos'] = [v for v in data.get('hero_videos', []) if v['id'] != vid]
    save_content('home', data)
    flash('Hero video deleted.', 'success')
    return redirect(url_for('admin.home_page'))

# ── about page ───────────────────────────────────────────────────────────────

@admin_bp.route('/about')
@login_required
def about_page():
    return render_template('admin/about_page.html', active='about',
                           data=load('about', {}))

@admin_bp.route('/about/save-story', methods=['POST'])
@login_required
def save_about_story():
    data = load('about', {})
    data['story'] = {k: request.form.get(k, '') for k in
                     ('para1_en', 'para1_ar', 'para2_en', 'para2_ar', 'pull_ar')}
    save_content('about', data)
    flash('Our Story saved.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/save-goals', methods=['POST'])
@login_required
def save_about_goals():
    data = load('about', {})
    title_en = request.form.getlist('strategic_title_en')
    title_ar = request.form.getlist('strategic_title_ar')
    text_en  = request.form.getlist('strategic_text_en')
    text_ar  = request.form.getlist('strategic_text_ar')
    icon     = request.form.getlist('strategic_icon')
    strategic = [
        {'title_en': title_en[i], 'title_ar': title_ar[i],
         'text_en': text_en[i], 'text_ar': text_ar[i], 'icon': icon[i]}
        for i in range(len(title_en))
    ]
    data['goals'] = {'strategic': strategic}
    save_content('about', data)
    flash('Goals saved.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/values/add', methods=['POST'])
@login_required
def about_value_add():
    data   = load('about', {})
    values = data.get('values', [])
    new_id = max((v['id'] for v in values), default=0) + 1
    try:
        order = int(request.form.get('order', len(values) + 1))
    except ValueError:
        order = len(values) + 1
    values.append({
        'id': new_id,
        'title_en': request.form.get('title_en', ''),
        'title_ar': request.form.get('title_ar', ''),
        'text_en': request.form.get('text_en', ''),
        'text_ar': request.form.get('text_ar', ''),
        'icon': request.form.get('icon', ''),
        'visible': request.form.get('visible') == 'on',
        'order': order,
    })
    data['values'] = values
    save_content('about', data)
    flash('Value added.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/values/edit/<int:vid>', methods=['POST'])
@login_required
def about_value_edit(vid):
    data = load('about', {})
    for v in data.get('values', []):
        if v['id'] == vid:
            for k in ('title_en', 'title_ar', 'text_en', 'text_ar', 'icon'):
                v[k] = request.form.get(k, v.get(k, ''))
            v['visible'] = request.form.get('visible') == 'on'
            try:
                v['order'] = int(request.form.get('order', v.get('order', 0)))
            except ValueError:
                pass
            break
    save_content('about', data)
    flash('Value updated.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/values/delete/<int:vid>', methods=['POST'])
@login_required
def about_value_delete(vid):
    data = load('about', {})
    data['values'] = [v for v in data.get('values', []) if v['id'] != vid]
    save_content('about', data)
    flash('Value deleted.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/save-stats', methods=['POST'])
@login_required
def save_about_stats():
    data      = load('about', {})
    nums      = request.form.getlist('num')
    formats   = request.form.getlist('format')
    labels_en = request.form.getlist('label_en')
    labels_ar = request.form.getlist('label_ar')
    data['stats'] = [
        {'num': nums[i], 'format': formats[i],
         'label_en': labels_en[i], 'label_ar': labels_ar[i]}
        for i in range(len(nums))
    ]
    save_content('about', data)
    flash('Stats saved.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/save-partners', methods=['POST'])
@login_required
def save_about_partners():
    data = load('about', {})
    role_en  = request.form.getlist('partner_role_en')
    role_ar  = request.form.getlist('partner_role_ar')
    title_en = request.form.getlist('partner_title_en')
    title_ar = request.form.getlist('partner_title_ar')
    text_en  = request.form.getlist('partner_text_en')
    text_ar  = request.form.getlist('partner_text_ar')
    cards = [
        {'role_en': role_en[i], 'role_ar': role_ar[i],
         'title_en': title_en[i], 'title_ar': title_ar[i],
         'text_en': text_en[i], 'text_ar': text_ar[i]}
        for i in range(len(role_en))
    ]
    data['partners'] = {
        'intro_en': request.form.get('intro_en', ''),
        'intro_ar': request.form.get('intro_ar', ''),
        'cards': cards,
    }
    save_content('about', data)
    flash('Partners & Awards saved.', 'success')
    return redirect(url_for('admin.about_page'))

@admin_bp.route('/about/save-cta', methods=['POST'])
@login_required
def save_about_cta():
    data = load('about', {})
    data['cta_en'] = request.form.get('cta_en', '')
    data['cta_ar'] = request.form.get('cta_ar', '')
    save_content('about', data)
    flash('CTA text saved.', 'success')
    return redirect(url_for('admin.about_page'))

# ── music / albums ───────────────────────────────────────────────────────────

@admin_bp.route('/music')
@login_required
def music_page():
    return render_template('admin/music_page.html', active='music',
                           data=load('music', {'items': [], 'display_limit': 12}))

@admin_bp.route('/music/save-limit', methods=['POST'])
@login_required
def music_save_limit():
    data = load('music', {'items': []})
    try:
        data['display_limit'] = int(request.form.get('display_limit', 12))
    except ValueError:
        data['display_limit'] = 12
    save_content('music', data)
    flash('Display limit saved.', 'success')
    return redirect(url_for('admin.music_page'))

@admin_bp.route('/music/add', methods=['POST'])
@login_required
def music_add():
    data  = load('music', {'items': []})
    items = data.get('items', [])
    base_id = secure_filename(request.form.get('title_en', 'item')).lower() or 'item'
    new_id = base_id
    n = 1
    existing_ids = {i['id'] for i in items}
    while new_id in existing_ids:
        n += 1
        new_id = '{}-{}'.format(base_id, n)

    cover = ''
    f = request.files.get('cover')
    if f and f.filename and _allowed(f.filename, ALLOWED_IMG):
        fname = 'music_{}_{}'.format(new_id, secure_filename(f.filename))
        dest  = os.path.join(_upload_dir(), 'music', fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        f.save(dest)
        cover = '/static/uploads/music/' + fname

    try:
        order = int(request.form.get('order', len(items) + 1))
    except ValueError:
        order = len(items) + 1

    items.append({
        'id': new_id,
        'type': request.form.get('type', 'album'),
        'artist': request.form.get('artist', 'unspecified'),
        'title_en': request.form.get('title_en', ''),
        'title_ar': request.form.get('title_ar', ''),
        'subtitle_en': request.form.get('subtitle_en', ''),
        'subtitle_ar': request.form.get('subtitle_ar', ''),
        'cover': cover,
        'link': request.form.get('link', ''),
        'visible': request.form.get('visible') == 'on',
        'order': order,
    })
    data['items'] = items
    save_content('music', data)
    flash('Album/single added.', 'success')
    return redirect(url_for('admin.music_page'))

@admin_bp.route('/music/edit/<item_id>', methods=['POST'])
@login_required
def music_edit(item_id):
    data = load('music', {'items': []})
    for item in data.get('items', []):
        if item['id'] == item_id:
            for k in ('type', 'artist', 'title_en', 'title_ar',
                      'subtitle_en', 'subtitle_ar', 'link'):
                item[k] = request.form.get(k, item.get(k, ''))
            item['visible'] = request.form.get('visible') == 'on'
            try:
                item['order'] = int(request.form.get('order', item.get('order', 0)))
            except ValueError:
                pass
            f = request.files.get('cover')
            if f and f.filename and _allowed(f.filename, ALLOWED_IMG):
                fname = 'music_{}_{}'.format(item_id, secure_filename(f.filename))
                dest  = os.path.join(_upload_dir(), 'music', fname)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                f.save(dest)
                item['cover'] = '/static/uploads/music/' + fname
            break
    save_content('music', data)
    flash('Saved.', 'success')
    return redirect(url_for('admin.music_page'))

@admin_bp.route('/music/delete/<item_id>', methods=['POST'])
@login_required
def music_delete(item_id):
    data = load('music', {'items': []})
    data['items'] = [i for i in data.get('items', []) if i['id'] != item_id]
    save_content('music', data)
    flash('Deleted.', 'success')
    return redirect(url_for('admin.music_page'))

# ── calendar ─────────────────────────────────────────────────────────────────

CALENDAR_FIELDS = ('title_en', 'title_ar', 'date', 'end_date', 'time',
                   'location_en', 'location_ar', 'description_en',
                   'description_ar', 'link')

@admin_bp.route('/calendar')
@login_required
def calendar_page():
    return render_template('admin/calendar_page.html', active='calendar',
                           data=load('calendar', {'events': []}))

@admin_bp.route('/calendar/add', methods=['POST'])
@login_required
def calendar_add():
    data   = load('calendar', {'events': []})
    events = data.get('events', [])
    new_id = max((e['id'] for e in events), default=0) + 1
    events.append({
        'id': new_id,
        **{k: request.form.get(k, '') for k in CALENDAR_FIELDS},
        'visible': request.form.get('visible') == 'on',
    })
    data['events'] = events
    save_content('calendar', data)
    flash('Event added.', 'success')
    return redirect(url_for('admin.calendar_page'))

@admin_bp.route('/calendar/edit/<int:eid>', methods=['POST'])
@login_required
def calendar_edit(eid):
    data = load('calendar', {'events': []})
    for e in data.get('events', []):
        if e['id'] == eid:
            for k in CALENDAR_FIELDS:
                e[k] = request.form.get(k, e.get(k, ''))
            e['visible'] = request.form.get('visible') == 'on'
            break
    save_content('calendar', data)
    flash('Event updated.', 'success')
    return redirect(url_for('admin.calendar_page'))

@admin_bp.route('/calendar/delete/<int:eid>', methods=['POST'])
@login_required
def calendar_delete(eid):
    data = load('calendar', {'events': []})
    data['events'] = [e for e in data.get('events', []) if e['id'] != eid]
    save_content('calendar', data)
    flash('Event deleted.', 'success')
    return redirect(url_for('admin.calendar_page'))

# ── choirs page ──────────────────────────────────────────────────────────────

@admin_bp.route('/choirs')
@login_required
def choirs_page():
    return render_template('admin/choirs_page.html', active='choirs',
                           data=load('audio', {'tracks': []}),
                           choirs_text=load('choirs', {}))

@admin_bp.route('/choirs/save-text', methods=['POST'])
@login_required
def save_choirs_text():
    data = load('choirs', {})
    data['gardenia'] = {k: request.form.get('gardenia_' + k, '') for k in
                        ('desc_en', 'desc_ar', 'achievements_en', 'achievements_ar')}
    data['tanaghom'] = {k: request.form.get('tanaghom_' + k, '') for k in
                        ('desc_en', 'desc_ar', 'get_involved_en', 'get_involved_ar')}
    save_content('choirs', data)
    flash('Choir descriptions saved.', 'success')
    return redirect(url_for('admin.choirs_page'))

@admin_bp.route('/choirs/save-track/<track_id>', methods=['POST'])
@login_required
def save_track(track_id):
    data = load('audio', {'tracks': []})
    for t in data.get('tracks', []):
        if t['id'] == track_id:
            for k in ('label_en','label_ar','title','composer_en','composer_ar','duration'):
                t[k] = request.form.get(k, t.get(k, ''))
            f = request.files.get('audio_file')
            if f and f.filename and _allowed(f.filename, ALLOWED_AUDIO):
                fname = 'track_{}_{}'.format(track_id, secure_filename(f.filename))
                dest  = os.path.join(_upload_dir(), 'audio', fname)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                f.save(dest)
                t['file'] = '/static/uploads/audio/' + fname
            break
    save_content('audio', data)
    flash('Track saved.', 'success')
    return redirect(url_for('admin.choirs_page'))

# ── gallery ──────────────────────────────────────────────────────────────────

@admin_bp.route('/gallery/upload-temp', methods=['POST'])
@login_required
def gallery_upload_temp():
    """Upload a single image, compress + resize, return its path as JSON."""
    import time
    from flask import jsonify
    f = request.files.get('file')
    if not f or not f.filename or not _allowed(f.filename, ALLOWED_IMG):
        return jsonify({'error': 'invalid file'}), 400
    fname = 'tmp_{}_{}.jpg'.format(int(time.time() * 1000), secure_filename(f.filename)[:20])
    dest  = os.path.join(_upload_dir(), 'gallery', fname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        from PIL import Image as PILImage, ExifTags
        img = PILImage.open(f)
        # Auto-rotate based on EXIF orientation
        try:
            for tag, val in img._getexif().items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    if val == 3:   img = img.rotate(180, expand=True)
                    elif val == 6: img = img.rotate(270, expand=True)
                    elif val == 8: img = img.rotate(90, expand=True)
                    break
        except Exception:
            pass
        img = img.convert('RGB')
        w, h = img.size
        max_dim = 1920
        if w > max_dim or h > max_dim:
            ratio = min(max_dim / w, max_dim / h)
            img = img.resize((int(w * ratio), int(h * ratio)), PILImage.LANCZOS)
        img.save(dest, 'JPEG', quality=82, optimize=True)
    except Exception:
        f.seek(0)
        f.save(dest)
    return jsonify({'path': '/static/uploads/gallery/' + fname})

@admin_bp.route('/gallery')
@login_required
def gallery_page():
    return render_template('admin/gallery_page.html', active='gallery',
                           data=load('gallery', {'items': []}))

@admin_bp.route('/gallery/save-press', methods=['POST'])
@login_required
def gallery_save_press():
    data = load('gallery', {'items': []})
    data['press'] = {
        'text_en': request.form.get('text_en', ''),
        'text_ar': request.form.get('text_ar', ''),
    }
    save_content('gallery', data)
    flash('Press text saved.', 'success')
    return redirect(url_for('admin.gallery_page'))

@admin_bp.route('/gallery/upload-video-temp', methods=['POST'])
@login_required
def gallery_upload_video_temp():
    """Upload a single video and return its path as JSON."""
    import time
    from flask import jsonify
    f = request.files.get('file')
    if not f or not f.filename or not _allowed(f.filename, ALLOWED_VIDEO):
        return jsonify({'error': 'invalid file'}), 400
    ext   = f.filename.rsplit('.', 1)[1].lower()
    fname = 'tmp_vid_{}_{}.{}'.format(int(time.time() * 1000), secure_filename(f.filename)[:20], ext)
    dest  = os.path.join(_upload_dir(), 'gallery', fname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    f.save(dest)
    return jsonify({'path': '/static/uploads/gallery/' + fname})

@admin_bp.route('/gallery/add', methods=['POST'])
@login_required
def gallery_add():
    data   = load('gallery', {'items': []})
    items  = data.get('items', [])
    new_id = max((i['id'] for i in items), default=0) + 1

    # Accept pre-uploaded temp paths (from sequential JS uploader)
    images = [p for p in request.form.getlist('pre_images') if p.startswith('/static/uploads/gallery/')]

    # Also accept direct file uploads (fallback)
    for idx, f in enumerate(request.files.getlist('images')):
        if f and f.filename and _allowed(f.filename, ALLOWED_IMG):
            ext   = f.filename.rsplit('.', 1)[1].lower()
            fname = 'gallery_{}_{}.{}'.format(new_id, len(images) + idx, ext)
            dest  = os.path.join(_upload_dir(), 'gallery', fname)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            f.save(dest)
            images.append('/static/uploads/gallery/' + fname)

    video = ''
    vf = request.files.get('video')
    if vf and vf.filename and _allowed(vf.filename, ALLOWED_VIDEO):
        ext   = vf.filename.rsplit('.', 1)[1].lower()
        fname = 'gallery_video_{}.{}'.format(new_id, ext)
        dest  = os.path.join(_upload_dir(), 'gallery', fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        vf.save(dest)
        video = '/static/uploads/gallery/' + fname
    if not video:
        pv = request.form.get('pre_video', '')
        if pv.startswith('/static/uploads/gallery/'):
            video = pv

    cover = ''
    pc = request.form.get('pre_cover', '')
    if pc.startswith('/static/uploads/gallery/'):
        cover = pc

    date_raw = request.form.get('date_raw', '')
    date_en, date_ar_auto = _format_date(date_raw)
    date_ar = request.form.get('dateAr', '') or date_ar_auto
    year    = date_raw[:4] if date_raw else request.form.get('year', '')

    items.append({
        'id':       new_id,
        'title':    request.form.get('title', ''),
        'titleAr':  request.form.get('titleAr', ''),
        'date':     date_en,
        'dateAr':   date_ar,
        'venue':    request.form.get('venue', ''),
        'venueAr':  request.form.get('venueAr', ''),
        'ensemble': request.form.get('ensemble', 'gardenia'),
        'type':     request.form.get('type', 'concert'),
        'year':     year,
        'size':     request.form.get('size', 'normal'),
        'image':    images[0] if images else '',
        'images':   images,
        'video':    video,
        'cover':    cover,
        'palette':  ['#2a3d28', '#8DA086', '#F5D000'],
    })
    data['items'] = items
    save_content('gallery', data)
    flash('Gallery item added.', 'success')
    return redirect(url_for('admin.gallery_page'))

@admin_bp.route('/gallery/edit/<int:item_id>', methods=['POST'])
@login_required
def gallery_edit(item_id):
    data = load('gallery', {'items': []})
    for item in data.get('items', []):
        if item['id'] == item_id:
            for k in ('title','titleAr','dateAr','venue','venueAr','ensemble','type','size'):
                item[k] = request.form.get(k, item.get(k, ''))

            date_raw = request.form.get('date_raw', '')
            if date_raw:
                date_en, date_ar_auto = _format_date(date_raw)
                item['date'] = date_en
                item['year'] = date_raw[:4]
                if not request.form.get('dateAr'):
                    item['dateAr'] = date_ar_auto

            # Images: keep checked existing + add new uploads
            kept   = set(request.form.getlist('keep_image'))
            old    = item.get('images', [item['image']] if item.get('image') else [])
            images = [img for img in old if img in kept] if kept else list(old)

            # Accept pre-uploaded temp paths from sequential JS uploader
            pre = [p for p in request.form.getlist('pre_images') if p.startswith('/static/uploads/gallery/')]
            images.extend(pre)

            base_idx = len(images)
            for idx, f in enumerate(request.files.getlist('images')):
                if f and f.filename and _allowed(f.filename, ALLOWED_IMG):
                    ext   = f.filename.rsplit('.', 1)[1].lower()
                    fname = 'gallery_{}_{}.{}'.format(item_id, base_idx + idx, ext)
                    dest  = os.path.join(_upload_dir(), 'gallery', fname)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    f.save(dest)
                    images.append('/static/uploads/gallery/' + fname)
            item['images'] = images
            item['image']  = images[0] if images else ''

            vf = request.files.get('video')
            if vf and vf.filename and _allowed(vf.filename, ALLOWED_VIDEO):
                ext   = vf.filename.rsplit('.', 1)[1].lower()
                fname = 'gallery_video_{}.{}'.format(item_id, ext)
                dest  = os.path.join(_upload_dir(), 'gallery', fname)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                vf.save(dest)
                item['video'] = '/static/uploads/gallery/' + fname
            elif request.form.get('remove_video'):
                item['video'] = ''
            else:
                pv = request.form.get('pre_video', '')
                if pv.startswith('/static/uploads/gallery/'):
                    item['video'] = pv

            pc = request.form.get('pre_cover', '')
            if pc.startswith('/static/uploads/gallery/'):
                item['cover'] = pc
            elif request.form.get('remove_cover'):
                item['cover'] = ''
            break
    save_content('gallery', data)
    flash('Gallery item updated.', 'success')
    return redirect(url_for('admin.gallery_page'))

@admin_bp.route('/gallery/delete/<int:item_id>', methods=['POST'])
@login_required
def gallery_delete(item_id):
    data = load('gallery', {'items': []})
    data['items'] = [i for i in data.get('items', []) if i['id'] != item_id]
    save_content('gallery', data)
    flash('Gallery item deleted.', 'success')
    return redirect(url_for('admin.gallery_page'))

@admin_bp.route('/gallery/bulk-delete', methods=['POST'])
@login_required
def gallery_bulk_delete():
    ids  = set(int(i) for i in request.form.getlist('ids') if i.isdigit())
    data = load('gallery', {'items': []})
    removed = len([i for i in data.get('items', []) if i['id'] in ids])
    data['items'] = [i for i in data.get('items', []) if i['id'] not in ids]
    save_content('gallery', data)
    flash('Deleted {} item(s).'.format(removed), 'success')
    return redirect(url_for('admin.gallery_page'))

# ── settings ─────────────────────────────────────────────────────────────────

@admin_bp.route('/settings')
@login_required
def settings_page():
    return render_template('admin/settings_page.html', active='settings',
                           data=load('settings', {}))

@admin_bp.route('/settings/save', methods=['POST'])
@login_required
def settings_save():
    import time
    data = load('settings', {})
    for k in ('site_name_en', 'site_name_ar',
              'contact_email', 'press_email', 'address_en', 'address_ar',
              'social_instagram', 'social_facebook', 'social_youtube',
              'footer_tagline_en', 'footer_tagline_ar'):
        data[k] = request.form.get(k, data.get(k, ''))

    f = request.files.get('logo')
    if f and f.filename and _allowed(f.filename, ALLOWED_IMG):
        ext   = f.filename.rsplit('.', 1)[1].lower()
        fname = 'logo_{}.{}'.format(int(time.time()), ext)
        dest  = os.path.join(_upload_dir(), 'branding', fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        f.save(dest)
        data['logo'] = '/static/uploads/branding/' + fname

    save_content('settings', data)
    flash('Settings saved.', 'success')
    return redirect(url_for('admin.settings_page'))

# ── publish ──────────────────────────────────────────────────────────────────

@admin_bp.route('/publish', methods=['POST'])
@login_required
def publish():
    try:
        root   = _project_root()
        build  = os.path.join(root, 'backend', 'build.py')
        dist   = os.path.join(root, 'dist')
        deploy = os.path.expanduser('~/tanaghomgardenia.org')

        result = subprocess.run(
            ['python3', build, '--domain'],
            capture_output=True, text=True, cwd=root
        )
        if result.returncode != 0:
            flash('Build failed: ' + result.stderr[:400], 'error')
            return redirect(url_for('admin.dashboard'))

        if os.path.isdir(deploy):
            for item in os.listdir(dist):
                s = os.path.join(dist, item)
                d = os.path.join(deploy, item)
                if os.path.isdir(s):
                    if os.path.exists(d):
                        shutil.rmtree(d)
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            flash('Site published and deployed successfully.', 'success')
        else:
            flash('Build complete. Copy dist/ manually to deploy.', 'success')
    except Exception as e:
        flash('Publish error: ' + str(e), 'error')
    return redirect(url_for('admin.dashboard'))
