import os
import shutil
import subprocess
from functools import wraps
from flask import (Blueprint, render_template, request, session,
                   redirect, url_for, flash, current_app)
from werkzeug.utils import secure_filename
from ..content import load, save as save_content

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ── helpers ──────────────────────────────────────────────────────────────────

def _upload_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, '..', '..', '..', 'frontend', 'static', 'uploads'))

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
        pw = request.form.get('password', '')
        if pw == current_app.config.get('ADMIN_PASSWORD', 'tanaghom2024'):
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
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

# ── about page ───────────────────────────────────────────────────────────────

@admin_bp.route('/about')
@login_required
def about_page():
    return render_template('admin/about_page.html', active='about',
                           data=load('about', {}))

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

# ── choirs page ──────────────────────────────────────────────────────────────

@admin_bp.route('/choirs')
@login_required
def choirs_page():
    return render_template('admin/choirs_page.html', active='choirs',
                           data=load('audio', {'tracks': []}))

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

@admin_bp.route('/gallery')
@login_required
def gallery_page():
    return render_template('admin/gallery_page.html', active='gallery',
                           data=load('gallery', {'items': []}))

@admin_bp.route('/gallery/add', methods=['POST'])
@login_required
def gallery_add():
    data   = load('gallery', {'items': []})
    items  = data.get('items', [])
    new_id = max((i['id'] for i in items), default=0) + 1

    images = []
    for idx, f in enumerate(request.files.getlist('images')):
        if f and f.filename and _allowed(f.filename, ALLOWED_IMG):
            ext   = f.filename.rsplit('.', 1)[1].lower()
            fname = 'gallery_{}_{}.{}'.format(new_id, idx, ext)
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
    save_content('settings', {
        k: request.form.get(k, '') for k in
        ('contact_email','press_email','address_en','address_ar',
         'social_instagram','social_facebook','social_youtube',
         'footer_tagline_en','footer_tagline_ar')
    })
    flash('Settings saved.', 'success')
    return redirect(url_for('admin.settings_page'))

# ── publish ──────────────────────────────────────────────────────────────────

@admin_bp.route('/publish', methods=['POST'])
@login_required
def publish():
    try:
        here   = os.path.dirname(os.path.abspath(__file__))
        root   = os.path.normpath(os.path.join(here, '..', '..', '..'))
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
