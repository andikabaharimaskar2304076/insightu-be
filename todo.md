
# 🛠️ Back-End To-Do List - InsightU (Django + DRF)

Berikut adalah daftar tugas detail untuk pengembangan back-end berdasarkan fitur prioritas InsightU.

---

## 1. 🧑‍💼 Autentikasi & Manajemen Pengguna

### Tujuan
Pengguna dapat mendaftar, login, dan dibedakan berdasarkan peran (student, psychologist, admin).

### To-Do
- [ ] Buat model `User` kustom (`AbstractUser`) dengan `email`, `role`, `is_verified`
- [ ] Set `AUTH_USER_MODEL` di `settings.py`
- [ ] Buat serializer:
  - [ ] `RegisterSerializer`
  - [ ] `LoginSerializer` (gunakan JWT)
- [ ] Endpoint:
  - [ ] `POST /api/register`
  - [ ] `POST /api/token/`
  - [ ] `GET /api/me/`
- [ ] Middleware/decorator untuk cek `role`
- [ ] Admin panel untuk verifikasi akun

---

## 2. 📘 Profil Siswa & Psikolog

### Tujuan
Pisahkan informasi tambahan untuk siswa dan psikolog.

### To-Do
- [ ] Model:
  - [ ] `StudentProfile` (OneToOne ke `User`)
  - [ ] `PsychologistProfile` (OneToOne ke `User`)
- [ ] Serializer:
  - [ ] `StudentProfileSerializer`
  - [ ] `PsychologistProfileSerializer`
- [ ] Endpoint:
  - [ ] `GET/PUT /api/profile/student/`
  - [ ] `GET/PUT /api/profile/psychologist/`

---

## 3. 🗓️ Manajemen Sesi Konseling

### Tujuan
Mahasiswa mengajukan sesi, psikolog merespons.

### To-Do
- [ ] Model `Session`:
  - `student`, `psychologist`, `schedule_time`, `status`, `notes`
- [ ] `SessionSerializer`
- [ ] Permission:
  - Mahasiswa hanya lihat/buat sesi miliknya
  - Psikolog hanya bisa respon sesi miliknya
- [ ] Endpoint:
  - [ ] `POST /api/sessions/`
  - [ ] `GET /api/sessions/`
  - [ ] `PATCH /api/sessions/<id>/`

---

## 4. 🔔 Notifikasi

### Tujuan
Memberi tahu pengguna tentang status sesi.

### To-Do
- [ ] Model `Notification`
- [ ] Serializer `NotificationSerializer`
- [ ] Endpoint:
  - [ ] `GET /api/notifications/`
  - [ ] `PATCH /api/notifications/<id>/read/`
- [ ] Tambahkan notifikasi otomatis saat:
  - [ ] Sesi dibuat
  - [ ] Sesi disetujui/ditolak

---

## 5. ✅ Verifikasi Akun oleh Admin

### Tujuan
Admin memverifikasi akun baru.

### To-Do
- [ ] Tambahkan field `is_verified` di `User`
- [ ] Endpoint:
  - [ ] `GET /api/admin/users?unverified=true`
  - [ ] `PATCH /api/admin/users/<id>/verify/`
- [ ] Batasi hanya admin

---

## 6. 📑 Log Aktivitas Sesi (Opsional)

### Tujuan
Mencatat perubahan status sesi.

### To-Do
- [ ] Model `SessionLog`
- [ ] Log otomatis saat sesi dibuat / diubah
- [ ] Endpoint opsional: `GET /api/sessions/<id>/logs/`

---

## ⚙️ Konfigurasi & Umum

- [ ] Setup JWT dengan `SimpleJWT`
- [ ] Aktifkan `django-cors-headers` untuk frontend
- [ ] Gunakan `.env` + `python-dotenv` untuk config rahasia
- [ ] Setup MySQL di `settings.py`
- [ ] Dokumentasi API: `drf-yasg` / `drf-spectacular`
