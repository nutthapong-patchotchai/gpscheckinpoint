# UP Checkin Point

ระบบเช็คอินพิกัดสำหรับใช้งาน local ด้วย Django templates, Django auth มาตรฐาน, ข้อมูลหอพัก, แผนที่จังหวัดพะเยา, และระบบเหรียญสำหรับแลกชั่วโมงกิจกรรม

โปรเจกต์นี้ถูกปรับจากแนว frontend แยก/social login ให้กลับมาเป็นเว็บ Django ที่รันง่ายในเครื่องเดียว เปิดแล้วใช้งานได้ทันที เหมาะสำหรับ demo, ส่งงาน, ทดลอง flow ระบบเช็คอิน หรือพัฒนาต่อเป็นระบบกิจกรรมนิสิต

---

## สรุประบบ

UP Checkin Point คือระบบที่ให้ผู้ใช้สมัครสมาชิก, เข้าสู่ระบบ, เช็คอินตำแหน่งปัจจุบัน, บันทึกสถานที่และอาการ, ดูประวัติย้อนหลังบนแผนที่พะเยา, สะสมเหรียญจากการเช็คอิน และแลกเหรียญเป็นชั่วโมงกิจกรรม

ฟีเจอร์หลัก:

- หน้าเว็บทั้งหมดใช้ Django templates
- Auth เป็น username/password ของ Django ปกติ
- สมัครสมาชิกผ่านหน้า form จริง
- เช็คอินด้วย latitude/longitude
- อ่านตำแหน่งจาก browser geolocation
- เติมชื่อสถานที่และที่อยู่จากข้อมูลหอพักใกล้เคียงโดยอัตโนมัติ
- ประวัติผู้ใช้มีชื่อ, คณะ, หอพักปัจจุบัน, สถานที่เช็คอิน และอาการ
- แผนที่จำลองจังหวัดพะเยา แสดงจุดเช็คอิน 14 วันย้อนหลัง
- ศูนย์ COVID timeline สำหรับเจ้าหน้าที่ระบุเคสและไล่ประวัติย้อนหลัง
- ระบบหา contact จากสถานที่ พิกัด วันเวลา และหอพักใน scope มหาวิทยาลัยพะเยา
- Export timeline/contact เป็น CSV สำหรับส่งต่อเจ้าหน้าที่
- Mock data จังหวัดพะเยา, อำเภอ, ตำบล, หอพัก และจุดเช็คอิน
- ระบบเหรียญจากการเช็คอินวันละครั้ง
- ระบบ streak เช็คอินต่อเนื่องเพื่อรับ bonus
- หน้าแลกเหรียญเป็นชั่วโมงกิจกรรม
- Django admin สำหรับดูแลข้อมูลหลัก
- REST API เดิมยังอยู่สำหรับใช้งานร่วมกับระบบอื่น

---

## Tech Stack

| ส่วน | รายละเอียด |
| --- | --- |
| Backend | Django 6.0.5 |
| API | Django REST Framework 3.17.1 |
| Database | SQLite by default |
| Frontend | Django Templates + CSS ในโปรเจกต์ |
| Auth | Django session auth + token auth สำหรับ API |
| Filtering | django-filter |
| Admin UI | django-admin-interface |
| ภาษา/เวลา | Thai, Asia/Bangkok |

---

## โครงสร้างโปรเจกต์

```text
gpscheckinpoint/
├── checkin/
│   ├── forms.py                         # ฟอร์มสมัครสมาชิกและเช็คอิน
│   ├── services.py                      # กติกาเหรียญ, streak, แลกชั่วโมงกิจกรรม
│   ├── models/
│   │   ├── address.py                   # ภูมิภาค จังหวัด อำเภอ ตำบล
│   │   ├── checkin.py                   # เช็คอิน, กระเป๋าเหรียญ, ธุรกรรม, รายการแลก
│   │   └── user.py                      # โปรไฟล์ผู้ใช้
│   ├── templates/
│   │   ├── base.html                    # layout หลัก
│   │   ├── checkin/
│   │   │   ├── home.html                # หน้าเช็คอิน
│   │   │   ├── history.html             # ประวัติ + แผนที่พะเยา
│   │   │   └── coins.html               # เหรียญและแลกชั่วโมงกิจกรรม
│   │   └── registration/                # login/register/logout templates
│   ├── static/css/site.css              # style หลักของ frontend
│   ├── serializer/                      # serializers สำหรับ API
│   └── views/                           # template views และ API views
├── dormitory/
│   ├── models.py                        # หอพัก รายละเอียด รูป เจ้าของ และ user dorm
│   ├── views.py                         # หน้าแสดงหอพัก
│   └── templates/dormitory/home.html
├── gpscheckin/
│   ├── settings.py
│   └── urls.py
├── requirements.txt
└── README.md
```

---

## Quick Start

ต้องใช้ Python 3.12 หรือใหม่กว่า

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py check
python manage.py migrate
python manage.py runserver
```

เปิดเว็บ:

```text
http://127.0.0.1:8000/
```

ถ้ามี virtualenv อยู่แล้วในโปรเจกต์นี้ สามารถใช้คำสั่งตรงๆ ได้:

```bash
./venv/bin/python manage.py runserver
```

---

## Environment Variables

ไฟล์ตัวอย่างอยู่ที่ `.env.example`

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
SQLITE_DB_PATH=db.sqlite3
```

ค่าที่ระบบอ่าน:

| ตัวแปร | ความหมาย | ค่า default |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | secret key สำหรับ Django | `dev-insecure-gpscheckin-change-me` |
| `DJANGO_DEBUG` | เปิด/ปิด debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | host ที่อนุญาตให้เข้าเว็บ | `localhost,127.0.0.1,[::1]` |
| `SQLITE_DB_PATH` | path ของ SQLite database | `db.sqlite3` |

หมายเหตุ: โปรเจกต์นี้ตั้งใจให้รัน local เป็นหลัก ถ้าจะ deploy จริงควรเปลี่ยน secret key, ปิด debug, ตั้ง allowed hosts และจัดการ static/media ให้เหมาะสม

---

## Local URLs

| URL | หน้า |
| --- | --- |
| `/` | หน้าแรก/รายการหอพัก |
| `/register/` | สมัครสมาชิก |
| `/accounts/login/` | เข้าสู่ระบบ |
| `/accounts/logout/` | ออกจากระบบ |
| `/checkin/` | เช็คอิน |
| `/checkin/history/` | ประวัติเช็คอินและแผนที่พะเยา |
| `/checkin/resolve-location/` | endpoint สำหรับเติมชื่อสถานที่จากพิกัด |
| `/coins/` | เหรียญ, รายการแลกของฉัน, แลกชั่วโมงกิจกรรม |
| `/tracing/` | ศูนย์ COVID timeline สำหรับเจ้าหน้าที่ |
| `/tracing/cases/new/` | เพิ่มเคส COVID-19 |
| `/admin/` | Django admin |
| `/api/` | API เดิมของระบบ checkin |
| `/api/dorm/` | API ของหอพัก |

---

## บัญชีทดสอบ

โปรเจกต์นี้ไม่ seed username/password หรือข้อมูลผู้ใช้จริงผ่าน migration เพื่อให้ปลอดภัยเมื่อนำขึ้น GitHub

หลังจาก clone โปรเจกต์และ migrate แล้ว ให้สร้าง admin local เอง:

```bash
python manage.py createsuperuser
```

ถ้าต้องการสร้างผู้ใช้ทดสอบทั่วไป ให้สมัครผ่านหน้า:

```text
http://127.0.0.1:8000/register/
```

---

## ระบบเช็คอิน

ผู้ใช้ที่ login แล้วสามารถเช็คอินได้ที่:

```text
/checkin/
```

ข้อมูลที่บันทึก:

- ผู้ใช้
- ชื่อสถานที่
- ที่อยู่สถานที่
- latitude
- longitude
- ภูมิภาค
- จังหวัด
- อำเภอ
- ตำบล
- อาการ เช่น มีไข้ ไอ มีน้ำมูก เจ็บคอ หายใจลำบาก ไม่ได้กลิ่น หรือปกติ
- วันที่และเวลาเช็คอิน
- เหรียญที่ได้รับจากเช็คอินนั้น
- streak ของวันนั้น

ปุ่ม `อ่านตำแหน่ง` ใช้ browser geolocation เพื่ออ่าน latitude/longitude จากเครื่องผู้ใช้ จากนั้นเรียก endpoint:

```text
/checkin/resolve-location/?lat=<latitude>&lng=<longitude>
```

ระบบจะค้นหาหอพักที่ใกล้พิกัดที่สุดจากข้อมูลในฐานข้อมูล แล้วเติมชื่อสถานที่, ที่อยู่, ภูมิภาค, จังหวัด, อำเภอ และตำบลให้อัตโนมัติ

---

## ประวัติและแผนที่พะเยา

หน้า:

```text
/checkin/history/
```

แสดงข้อมูลสำคัญของผู้ใช้:

- ชื่อผู้ใช้
- อีเมล
- คณะ
- หอพักปัจจุบัน
- เหรียญคงเหลือ
- streak
- ชั่วโมงกิจกรรมที่แลกแล้ว

แผนที่:

- แสดงเฉพาะจุดเช็คอิน 14 วันย้อนหลัง
- ใช้แผนที่จำลองจังหวัดพะเยาใน template
- จุดเช็คอินมีหมายเลขเรียงตามเวลา
- มีเส้น route เชื่อมตำแหน่งตามลำดับการเดินทาง
- จุดที่มีอาการจะแสดงด้วยสีเตือน

---

## COVID Timeline สำหรับเจ้าหน้าที่

หน้า:

```text
/tracing/
```

ผู้ใช้ที่เป็น staff สามารถบันทึกเคส COVID-19 แล้วระบบจะช่วยดึงประวัติเช็คอินของเคสนั้นตามช่วงวันที่ที่กำหนด ถ้าไม่กำหนดช่วงวันที่ ระบบจะใช้ย้อนหลัง 14 วันจากวันที่เริ่มมีอาการหรือวันที่ตรวจพบ

ระบบหา contact จากเงื่อนไขหลัก:

- สถานที่เดียวกันภายใน 4 ชั่วโมง = เสี่ยงสูง
- พิกัดใกล้กันไม่เกิน 100 เมตรภายใน 4 ชั่วโมง = เสี่ยงสูง
- สถานที่เดียวกันในวันเดียวกัน = เสี่ยงกลาง
- พิกัดใกล้กันไม่เกิน 250 เมตรในวันเดียวกัน = เสี่ยงกลาง
- อยู่หอพักเดียวกันกับเคส = เสี่ยงกลาง
- อยู่ตำบลเดียวกันหรือพื้นที่ใกล้เคียงในวันเดียวกัน = เสี่ยงต่ำ

หน้า detail ของเคสมีทั้งรายการผู้เกี่ยวข้อง, timeline ของเคส, และปุ่ม export CSV เพื่อส่งต่อเจ้าหน้าที่

---

## ระบบเหรียญและชั่วโมงกิจกรรม

หน้า:

```text
/coins/
```

กติกาเหรียญอยู่ที่ `checkin/services.py`

```text
BASE_CHECKIN_COINS = 10
STREAK_BONUS_PER_DAY = 2
MAX_STREAK_BONUS = 20
```

กติกาปัจจุบัน:

- เช็คอินครั้งแรกของวัน ได้เหรียญ
- เช็คอินซ้ำวันเดียวกัน บันทึกประวัติได้ แต่ไม่ได้เหรียญซ้ำ
- วันแรกได้ 10 เหรียญ
- เช็คอินต่อเนื่องได้ bonus เพิ่มวันละ 2 เหรียญ
- bonus สูงสุด 20 เหรียญ
- ดังนั้นรางวัลต่อครั้งสูงสุดคือ 30 เหรียญ

ตัวอย่าง:

| Streak | เหรียญที่ได้ |
| --- | ---: |
| 1 วัน | 10 |
| 2 วัน | 12 |
| 3 วัน | 14 |
| 7 วัน | 22 |
| 11 วัน | 30 |
| 14 วัน | 30 |

รายการแลกเริ่มต้น:

| รายการ | ใช้เหรียญ | ได้ชั่วโมง |
| --- | ---: | ---: |
| แลก 1 ชั่วโมงกิจกรรม | 100 | 1.0 |
| แลก 2 ชั่วโมงกิจกรรม | 180 | 2.0 |
| แลก 5 ชั่วโมงกิจกรรม | 420 | 5.0 |

หน้าเหรียญจัดลำดับให้เห็นชัด:

1. สรุปยอดเหรียญ
2. รายการแลกของฉัน
3. แพ็กสำหรับแลกชั่วโมงกิจกรรม
4. ประวัติเหรียญล่าสุด

---

## Mock Data

ข้อมูล mock ในฐานข้อมูล local สำหรับพัฒนาอาจถูกเตรียมให้โฟกัสที่จังหวัดพะเยา แต่ข้อมูลผู้ใช้และประวัติเช็คอินส่วนบุคคลไม่ควร commit ขึ้น GitHub

ข้อมูลพื้นที่:

- ภูมิภาค: ภาคเหนือ
- จังหวัด: พะเยา
- อำเภอ: 9 อำเภอ
- ตำบล: 68 ตำบล

ข้อมูลหอพัก:

- มีข้อมูลหอพัก mock ในพื้นที่พะเยา/แม่กา
- มีพิกัด latitude/longitude
- ใช้สำหรับค้นหาสถานที่ใกล้เคียงเมื่อกดอ่านตำแหน่ง

ข้อมูลที่ seed ผ่าน migration:

- รายการแลกเหรียญเป็นชั่วโมงกิจกรรมเริ่มต้น
- ไม่สร้าง username ทดสอบ
- ไม่สร้างประวัติเช็คอินส่วนบุคคล
- ไม่ผูกข้อมูลกับ primary key ของ database local

ถ้าต้องการ demo data แบบครบระบบในเครื่อง local ให้รัน:

```bash
python manage.py seed_demo_data
```

บัญชีที่สร้าง:

- `demo_admin` / `demo123456` สำหรับ admin, tracing, export CSV
- `demo_user` / `demo123456` สำหรับทดลอง check-in, history, coins, redeem

คำสั่งนี้จะสร้างข้อมูลหอพัก, ตัวเลือกหอพัก, โปรไฟล์, หอพักของนิสิต, ประวัติเช็คอิน, กระเป๋าเหรียญ, transaction, รายการแลกชั่วโมงกิจกรรม, แต้มสะสมเดิม, เคส COVID-19, contact หลายระดับความเสี่ยง และข้อมูลสำหรับหน้า timeline โดยรันซ้ำได้โดยไม่สร้างชุดข้อมูลหลักซ้ำ

ถ้าต้องการ mock เฉพาะหน้า COVID Timeline แบบไม่ตั้งรหัสผ่านผู้ใช้ mock ยังใช้ได้ด้วย:

```bash
python manage.py seed_timeline_mock
```

---

## API สำคัญ

Auth API:

| Method | URL | ความหมาย |
| --- | --- | --- |
| `POST` | `/api/auth/register/` | สมัครสมาชิก API |
| `POST` | `/api/auth/login/` | login API |
| `POST` | `/api/auth/logout/` | logout API |

Checkin API:

| Method | URL | ความหมาย |
| --- | --- | --- |
| `GET` / `POST` | `/api/gps/` | list/create check-in |
| `GET` / `PUT` / `DELETE` | `/api/gps/<id>` | detail/update/delete check-in |
| `GET` | `/api/gps/history/<user_id>/` | ประวัติเช็คอินของ user |
| `GET` | `/api/gps/exist/<user_id>/` | ตรวจว่ามีเช็คอินวันนี้หรือยัง |

Address API:

| Method | URL | ความหมาย |
| --- | --- | --- |
| `GET` | `/api/geo/` | ภูมิภาค |
| `GET` | `/api/province/` | จังหวัด |
| `GET` | `/api/amphur/` | อำเภอ |
| `GET` | `/api/district/` | ตำบล |

Coin API:

| Method | URL | ความหมาย |
| --- | --- | --- |
| `GET` / `POST` | `/api/cut-coin/` | รายการแลก |
| `GET` / `POST` | `/api/user-cut-coin/` | แลกเหรียญเป็นชั่วโมงกิจกรรม |
| `GET` | `/api/getMyCoin/<user_id>/` | รายการแลกของผู้ใช้ |

เมื่อสร้าง check-in ผ่าน `/api/gps/` ระบบจะเรียกกติกาเหรียญเหมือนหน้าเว็บ ถ้าเป็นเช็คอินแรกของวันจะได้เหรียญและบันทึก transaction อัตโนมัติ

---

## คำสั่งที่ใช้บ่อย

ตรวจระบบ:

```bash
python manage.py check
```

สร้าง migration:

```bash
python manage.py makemigrations
```

รัน migration:

```bash
python manage.py migrate
```

ดู migration ของ checkin:

```bash
python manage.py showmigrations checkin
```

สร้าง admin:

```bash
python manage.py createsuperuser
```

เปลี่ยนรหัสผ่าน:

```bash
python manage.py changepassword <username>
```

รัน server:

```bash
python manage.py runserver
```

---

## Admin Guide

เข้า admin:

```text
http://127.0.0.1:8000/admin/
```

เมนูที่ควรดู:

- ผู้ใช้และสิทธิ์
- โปรไฟล์
- การเช็คอิน
- กระเป๋าเหรียญ
- ประวัติเหรียญ
- แลกแต้มสะสม
- แลกแต้มสะสมของนิสิต
- ภูมิภาค จังหวัด อำเภอ ตำบล
- หอพักและข้อมูลประกอบ

การเพิ่มรายการแลกใหม่:

1. เข้า admin
2. ไปที่ `แลกแต้มสะสม`
3. เพิ่มชื่อรายการ เช่น `แลก 3 ชั่วโมงกิจกรรม`
4. ใส่จำนวนเหรียญที่ต้องใช้
5. ใส่จำนวนชั่วโมงกิจกรรม
6. เปิด `status`

รายการที่เปิดใช้งานจะแสดงในหน้า `/coins/`

---

## Development Notes

ไฟล์สำคัญสำหรับพัฒนาต่อ:

| ไฟล์ | หน้าที่ |
| --- | --- |
| `checkin/forms.py` | ฟอร์มสมัครสมาชิกและเช็คอิน |
| `checkin/services.py` | business logic ของเหรียญและการแลก |
| `checkin/views/frontend.py` | views สำหรับ Django templates |
| `checkin/views/views.py` | DRF API views |
| `checkin/models/checkin.py` | check-in, wallet, transaction, reward models |
| `checkin/templates/checkin/coins.html` | หน้าเหรียญ |
| `checkin/templates/checkin/history.html` | ประวัติและแผนที่ |
| `checkin/static/css/site.css` | UI หลัก |
| `gpscheckin/urls.py` | route หลักของระบบ |

หลักการที่ควรรักษาไว้:

- หน้าเว็บหลักควรใช้ Django templates
- Auth หลักควรเป็น Django auth ธรรมดา
- Logic เหรียญควรอยู่ใน service ไม่กระจายใน views
- การเช็คอินจาก template และ API ต้องใช้กติกาเหรียญเดียวกัน
- Mock data พะเยาควรดูเป็นทางการและอ้างอิงกับจังหวัด/อำเภอ/ตำบลในระบบ

---

## Troubleshooting

### เข้าเว็บแล้วเจอ DisallowedHost

ตรวจ `DJANGO_ALLOWED_HOSTS` ใน `.env`

```env
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
```

### หน้าเว็บบอกตารางหรือ column ไม่มี

รัน migration:

```bash
python manage.py migrate
```

### Login ไม่ได้เพราะจำรหัสผ่านไม่ได้

เปลี่ยนรหัสผ่าน:

```bash
python manage.py changepassword <username>
```

### ไม่มีรายการแลกในหน้าเหรียญ

รัน migration ล่าสุดก่อน:

```bash
python manage.py migrate
```

หรือเพิ่มรายการเองจาก admin ในเมนู `แลกแต้มสะสม`

### อ่านตำแหน่งไม่ได้

สาเหตุที่พบบ่อย:

- Browser ไม่อนุญาต location permission
- ใช้ URL ที่ browser ไม่ถือว่าเป็น secure context
- เครื่องไม่มีข้อมูลตำแหน่ง
- ข้อมูลหอพัก mock ไม่มีพิกัดใกล้เคียง

สำหรับ local ให้เปิดด้วย:

```text
http://localhost:8000/checkin/
```

หรือ:

```text
http://127.0.0.1:8000/checkin/
```

---

## Roadmap ที่น่าทำต่อ

- เพิ่มหน้า profile ให้ผู้ใช้แก้ไขคณะและหอพักเอง
- เพิ่มหน้า admin dashboard สำหรับสรุปจำนวนเช็คอินต่อวัน
- เพิ่ม export รายงานเหรียญและชั่วโมงกิจกรรม
- เพิ่มระบบอนุมัติรายการแลกชั่วโมงกิจกรรม
- เพิ่มแผนที่จริงด้วย provider ภายนอกเมื่อพร้อมใช้งาน internet/API key
- เพิ่ม test case สำหรับ reward streak และ redeem flow
- เพิ่ม management command สำหรับ seed mock data ทั้งชุด

---

## สถานะปัจจุบัน

โปรเจกต์นี้พร้อมรัน local ด้วยคำสั่ง:

```bash
python manage.py runserver
```

จากนั้นเข้า:

```text
http://127.0.0.1:8000/
```

จุดเด่นของเวอร์ชันนี้คือระบบไม่ได้เป็นแค่หน้าฟอร์มเช็คอินแล้ว แต่มี flow ครบตั้งแต่สมัครสมาชิก, ระบุข้อมูลผู้ใช้, เช็คอิน, ดูประวัติบนแผนที่, สะสมเหรียญ, รักษา streak, แลกชั่วโมงกิจกรรม และตรวจสอบย้อนหลังผ่าน admin/API ได้ครบในโปรเจกต์เดียว
