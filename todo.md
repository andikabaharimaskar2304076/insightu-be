
# 🛠️ Back-End To-Do List - InsightU (Django + DRF)

Berikut adalah daftar tugas detail untuk pengembangan back-end berdasarkan fitur prioritas InsightU.

---

## 1. 🧑‍💼 Autentikasi & Manajemen Pengguna

### Tujuan
Pengguna dapat mendaftar, login, dan dibedakan berdasarkan peran (student, psychologist, admin).

### To-Do
- [v] Buat model `User` kustom (`AbstractUser`) dengan `email`, `role`, `is_verified`
- [v] Set `AUTH_USER_MODEL` di `settings.py`
- [v] Buat serializer:
  - [v] `RegisterSerializer`
  - [v] `LoginSerializer` (gunakan JWT)
- [v] Endpoint:
  - [v] `POST /api/register`
  - [v] `POST /api/token/`
  - [v] `GET /api/me/`
- [v] Middleware/decorator untuk cek `role`
- [ ] Admin panel untuk verifikasi akun

---

## 2. 📘 Profil Siswa & Psikolog

### Tujuan
Pisahkan informasi tambahan untuk siswa dan psikolog.

### To-Do
- [v] Model:
  - [v] `StudentProfile` (OneToOne ke `User`)
  - [v] `PsychologistProfile` (OneToOne ke `User`)
- [v] Serializer:
  - [v] `StudentProfileSerializer`
  - [v] `PsychologistProfileSerializer`
- [v] Endpoint:
  - [v] `GET/PUT /api/profile/student/`
  - [v] `GET/PUT /api/profile/psychologist/`

---

## 3. 🗓️ Manajemen Sesi Konseling

### Tujuan
Mahasiswa mengajukan sesi, psikolog merespons.

### To-Do
- [v] Model `Session`:
  - `student`, `psychologist`, `schedule_time`, `status`, `notes`
- [v] `SessionSerializer`
- [v] Permission:
  - Mahasiswa hanya lihat/buat sesi miliknya
  - Psikolog hanya bisa respon sesi miliknya
- [v] Endpoint:
  - [v] `POST /api/sessions/`
  - [v] `GET /api/sessions/`
  - [v] `PATCH /api/sessions/<id>/`

---

## 4. 🔔 Notifikasi

### Tujuan
Memberi tahu pengguna tentang status sesi.

### To-Do
- [v] Model `Notification`
- [v] Serializer `NotificationSerializer`
- [v] Endpoint:
  - [v] `GET /api/notifications/`
  - [v] `PATCH /api/notifications/<id>/read/`
- [v] Tambahkan notifikasi otomatis saat:
  - [v] Sesi dibuat
  - [v] Sesi disetujui/ditolak

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
