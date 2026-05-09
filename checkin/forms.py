from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User

from checkin.models.address import Amphur, District, Geography, Province
from checkin.models.checkin import CovidCase, gps
from checkin.models.user import profile


INPUT_CLASS = "form-control"


class StyledAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="ชื่อผู้ใช้หรืออีเมล",
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": INPUT_CLASS,
                "placeholder": "กรอกชื่อผู้ใช้หรืออีเมล",
            }
        ),
    )
    password = forms.CharField(
        label="รหัสผ่าน",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "class": INPUT_CLASS,
                "placeholder": "กรอกรหัสผ่าน",
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            auth_username = username
            if "@" in username:
                auth_username = (
                    User.objects.filter(email__iexact=username)
                    .values_list("username", flat=True)
                    .first()
                    or username
                )

            self.user_cache = authenticate(
                self.request,
                username=auth_username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class LocalUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label="ชื่อ",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "ชื่อ"}),
    )
    last_name = forms.CharField(
        label="นามสกุล",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "นามสกุล"}),
    )
    email = forms.EmailField(
        label="อีเมล",
        required=False,
        widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "name@example.com"}),
    )
    tel = forms.CharField(
        label="เบอร์โทร",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "08xxxxxxxx"}),
    )
    faculty = forms.CharField(
        label="คณะ",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "เช่น คณะเทคโนโลยีสารสนเทศและการสื่อสาร"}),
    )
    address = forms.CharField(
        label="ที่อยู่",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "บ้านเลขที่ ถนน หมู่บ้าน หรือรายละเอียดที่อยู่",
                "rows": 3,
            }
        ),
    )
    address2 = forms.CharField(
        label="หอพัก / ที่อยู่ปัจจุบัน",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "ชื่อหอพักหรือที่พัก"}),
    )
    post = forms.CharField(
        label="รหัสไปรษณีย์",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "รหัสไปรษณีย์"}),
    )
    geo = forms.ModelChoiceField(
        label="ภูมิภาค",
        queryset=Geography.objects.all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    province = forms.ModelChoiceField(
        label="จังหวัด",
        queryset=Province.objects.select_related("geo").all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    amphur = forms.ModelChoiceField(
        label="อำเภอ",
        queryset=Amphur.objects.select_related("province").all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    district = forms.ModelChoiceField(
        label="ตำบล",
        queryset=District.objects.select_related("amphur").all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": INPUT_CLASS,
                    "placeholder": "ชื่อผู้ใช้สำหรับเข้าสู่ระบบ",
                }
            ),
        }
        labels = {
            "username": "ชื่อผู้ใช้",
        }
        help_texts = {
            "username": "ใช้สำหรับเข้าสู่ระบบ ต้องไม่ซ้ำกับบัญชีที่มีอยู่",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update(
            {"class": INPUT_CLASS, "placeholder": "ตั้งรหัสผ่าน"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": INPUT_CLASS, "placeholder": "ยืนยันรหัสผ่าน"}
        )
        self.fields["password1"].label = "รหัสผ่าน"
        self.fields["password2"].label = "ยืนยันรหัสผ่าน"

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้สมัครแล้ว ลองเข้าสู่ระบบด้วยอีเมลนี้")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email", "")
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            self.save_profile(user)
        return user

    def save_profile(self, user):
        data = self.cleaned_data
        has_location = all(
            data.get(field)
            for field in ("geo", "province", "amphur", "district")
        )
        if not has_location:
            return None

        return profile.objects.create(
            user=user,
            address=data.get("address", ""),
            geo=data["geo"],
            province=data["province"],
            amphur=data["amphur"],
            district=data["district"],
            post=data.get("post", ""),
            tel=data.get("tel", ""),
            faculty=data.get("faculty", ""),
            question1=0,
            question2=0,
            question3=0,
            address2=data.get("address2", ""),
        )


class CheckinForm(forms.Form):
    place_name = forms.CharField(
        label="ชื่อสถานที่",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "เช่น หอพักแม่กา กรีนเพลส หรืออาคารเรียนรวม"}),
    )
    place_address = forms.CharField(
        label="ที่อยู่สถานที่",
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": INPUT_CLASS,
                "placeholder": "ระบบจะเติมที่อยู่จากสถานที่ใกล้ที่สุดให้",
                "rows": 2,
            }
        ),
    )
    latitude = forms.CharField(
        label="ละติจูด",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "ระบบจะกรอกให้อัตโนมัติ"}),
    )
    longitude = forms.CharField(
        label="ลองจิจูด",
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "ระบบจะกรอกให้อัตโนมัติ"}),
    )
    geo = forms.ModelChoiceField(
        label="ภูมิภาค",
        queryset=Geography.objects.all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    province = forms.ModelChoiceField(
        label="จังหวัด",
        queryset=Province.objects.select_related("geo").all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    amphur = forms.ModelChoiceField(
        label="อำเภอ",
        queryset=Amphur.objects.select_related("province").all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    district = forms.ModelChoiceField(
        label="ตำบล",
        queryset=District.objects.select_related("amphur").all().order_by("name"),
        required=False,
        empty_label="ไม่ระบุ",
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )
    sick1 = forms.BooleanField(label="มีไข้", required=False)
    sick2 = forms.BooleanField(label="ไอ", required=False)
    sick3 = forms.BooleanField(label="มีน้ำมูก", required=False)
    sick4 = forms.BooleanField(label="เจ็บคอ", required=False)
    sick5 = forms.BooleanField(label="หายใจเร็วหรือหายใจลำบาก", required=False)
    sick6 = forms.BooleanField(label="จมูกเริ่มไม่ได้กลิ่น", required=False)
    sick7 = forms.BooleanField(label="อาการปกติ", required=False)

    symptom_fields = ("sick1", "sick2", "sick3", "sick4", "sick5", "sick6", "sick7")

    def get_location_label(self):
        parts = []
        district = self.cleaned_data.get("district")
        amphur = self.cleaned_data.get("amphur")
        province = self.cleaned_data.get("province")
        if district:
            parts.append(f"ต.{district.name}")
        if amphur:
            parts.append(f"อ.{amphur.name}")
        if province:
            parts.append(f"จ.{province.name}")
        return " ".join(parts)

    def save(self, user):
        data = self.cleaned_data
        return gps.objects.create(
            user=user,
            place_name=data.get("place_name") or self.get_location_label(),
            place_address=data.get("place_address", ""),
            latitude=data.get("latitude") or 0,
            longitude=data.get("longitude") or 0,
            geo=data.get("geo"),
            province=data.get("province"),
            amphur=data.get("amphur"),
            district=data.get("district"),
            sick1=int(data.get("sick1")),
            sick2=int(data.get("sick2")),
            sick3=int(data.get("sick3")),
            sick4=int(data.get("sick4")),
            sick5=int(data.get("sick5")),
            sick6=int(data.get("sick6")),
            sick7=int(data.get("sick7")),
        )


class CovidCaseForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        label="ผู้ใช้",
        queryset=User.objects.all().order_by("username"),
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
    )

    class Meta:
        model = CovidCase
        fields = (
            "user",
            "status",
            "symptom_started_on",
            "confirmed_on",
            "trace_start_date",
            "trace_end_date",
            "notes",
        )
        labels = {
            "status": "สถานะเคส",
            "symptom_started_on": "วันที่เริ่มมีอาการ",
            "confirmed_on": "วันที่ตรวจพบ/ยืนยัน",
            "trace_start_date": "เริ่มไล่ timeline",
            "trace_end_date": "สิ้นสุดการไล่ timeline",
            "notes": "หมายเหตุ",
        }
        widgets = {
            "status": forms.Select(attrs={"class": INPUT_CLASS}),
            "symptom_started_on": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "confirmed_on": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "trace_start_date": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "trace_end_date": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "notes": forms.Textarea(
                attrs={
                    "class": INPUT_CLASS,
                    "rows": 4,
                    "placeholder": "เช่น รายละเอียดการสัมภาษณ์ หรือข้อสังเกตของเจ้าหน้าที่",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("trace_start_date")
        end_date = cleaned_data.get("trace_end_date")
        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError("วันที่สิ้นสุด timeline ต้องไม่อยู่ก่อนวันที่เริ่มต้น")
        return cleaned_data
