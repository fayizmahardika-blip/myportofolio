Nama : Fayiz Mahardika Ghulam Afandi 

NPM : 2506617374

Kelas : PBP F

## Tugas 1
1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti <section>, <article>, atau <aside>? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?

jawaban: ya saya menggunakan <section>, <article>. saya menggunakan section untuk untuk memisahkan bagian utama halaman dengan bagian experience pada porto saya, lalu article saya gunakan untuk merepresentasikan setiap item pengalaman secara terpisah.

2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?

jawaban: tantangan saya dalam membuat CSS responsive adalah menentukan layout yang tetap nyaman dibaca saat berpindah dari desktop ke mobile. Selain itu, saya juga masih kesulitan mengeksplorasi fitur CSS seperti `transition`, `transform`, hover effect, serta penggunaan library icon untuk media sosial. Karena itu, saya masih menggunakan bantuan AI untuk memahami fungsi-fungsi tersebut, lalu mencoba dan menyesuaikannya sendiri melalui browser sampai mendapatkan tampilan yang sesuai.

3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?

jawaban: karena website saat ini masih bersifat static, seluruh informasi masih dituliskan langsung di dalam HTML. Jika ingin menambahkan atau mengubah pengalaman, project, atau informasi lain, saya harus mengubah kode secara langsung. saya harap iterasi selanjutnya website dapat dikelola secara dinamis menggunakan database.


## AI Disclosure

Saya menggunakan ChatGPT untuk membantu memahami penggunaan HTML5 dan CSS3, terutama pada bagian CSS Grid, responsive design, hover effect, transition, serta penggunaan icon media sosial.

Saya menggunakan AI sebagai alat bantu untuk memahami fungsi property CSS yang belum saya ketahui. setelah mendapatkan saran, saya mencoba implementasinya langsung di browser dan melakukan penyesuaian manual pada layout, ukuran, warna, dan animasi agar sesuai dengan desain yang saya inginkan.


### Tugas 2

1. Ketika pengguna membuka halaman Education, request pertama kali diterima oleh `urls.py` pada project Django. `urls.py` project meneruskan request ke `urls.py` aplikasi `main`. Route `education/` kemudian menjalankan view `show_education`. View mengambil seluruh data dari model `Education` menggunakan `Education.objects.all()`, memasukkannya ke dalam context sebagai `education_list`, lalu meneruskannya ke template `education.html`. Template melakukan perulangan terhadap data tersebut dan menampilkannya pada browser.

2. Data Education sebaiknya disimpan pada model karena data menjadi terpusat dan dapat dikelola tanpa harus mengubah HTML setiap kali ada penambahan atau perubahan. Jika data ditulis langsung di template, setiap perubahan harus dilakukan secara manual pada HTML. Dengan model, data dapat ditambah, diubah, atau dihapus melalui database sehingga aplikasi lebih mudah dipelihara dan dikembangkan.

3. `makemigrations` digunakan untuk membuat file migration berdasarkan perubahan pada model, sedangkan `migrate` digunakan untuk menerapkan migration tersebut ke database. Contohnya, ketika saya menambahkan model `Education` beserta field seperti `institution`, `level`, `start_year`, dan field lainnya, saya menjalankan `python manage.py makemigrations` untuk membuat migration lalu `python manage.py migrate` untuk membuat struktur tabel tersebut pada database.


## AI Disclosure

Dalam pengerjaan Tugas 2, saya menggunakan ChatGPT sebagai alat bantu untuk memahami konsep Django dan membantu proses debugging selama pengembangan.

AI digunakan terutama untuk:
Memahami alur Model-View-Template (MVT) pada Django.
Membantu memahami hubungan antara `models.py`, `views.py`, `urls.py`, dan template HTML.
Membantu menyusun dan mengevaluasi model `Education`.
Memberikan contoh struktur template `education.html` dan penggunaan Django Template Language.
Membantu memahami dan membuat unit test untuk halaman Education.
Membantu debugging error pada deployment PWS, terutama terkait konfigurasi database dan environment variables.
Membantu menjelaskan penggunaan migration, Django shell, routing, dan penggunaan field pada model.
Membantu merapikan dokumentasi dan jawaban pertanyaan reflektif pada README.

Strategi prompting yang saya gunakan adalah memberikan konteks project, potongan kode, error message, serta instruksi tugas secara bertahap. Saya kemudian meminta penjelasan mengenai penyebab error, konsep yang digunakan, dan langkah penyelesaian agar tetap memahami proses implementasinya.

Seluruh kode yang digunakan tetap saya review, sesuaikan, dan jalankan sendiri pada project untuk memastikan implementasinya sesuai dengan kebutuhan tugas dan dapat berjalan dengan benar.



### Tugas 3

1. saya menggunakan ModelForm karena form dapat dibuat berdasarkan model yang sudah ada sehingga tidak perlu membuat seluruh input HTML secara manual. Selain itu, ModelForm juga membantu melakukan validasi data sesuai dengan field yang terdapat pada model. `{% csrf_token %}` diperlukan untuk melindungi form dari serangan CSRF, yaitu request yang dikirim oleh pihak lain dengan memanfaatkan sesi pengguna.

2. JSON lebih sering digunakan pada aplikasi web modern karena formatnya lebih sederhana dan ringkas dibandingkan XML. JSON juga lebih mudah diproses oleh JavaScript sehingga cocok digunakan untuk pertukaran data antara frontend dan backend. Selain itu, struktur JSON lebih mudah dibaca dan tidak membutuhkan banyak tag seperti pada XML.

3. pada project saya, view mengambil data Experience dari database menggunakan Django QuerySet. Karena object dari model Django tidak dapat langsung dikirim sebagai JSON, data tersebut harus melalui proses serialization terlebih dahulu. Serialization mengubah object Django menjadi format JSON yang dapat dikirim melalui `HttpResponse` dengan `content_type="application/json"`. Pada halaman Experience, data JSON tersebut kemudian di-deserialize kembali menjadi object agar dapat ditampilkan pada template.

#### AI Disclosure

dalam pengerjaan Tugas 3, saya menggunakan ChatGPT sebagai alat bantu untuk memahami implementasi ModelForm, CRUD, serta JSON serialization dan deserialization pada Django.

AI membantu saya dalam memahami perbedaan create dan update menggunakan `instance`, menyusun routing untuk model Experience yang menggunakan UUID, membuat fitur create, update, delete, dan JSON, serta membantu mengevaluasi unit test dan melakukan debugging ketika terdapat error.

strategi prompting yang saya gunakan adalah memberikan konteks project, potongan kode, struktur model, dan hasil implementasi secara bertahap. Setelah mendapatkan penjelasan atau contoh dari AI, saya menyesuaikannya kembali dengan struktur project saya.

setiap implementasi tetap saya cek dan jalankan sendiri menggunakan `python manage.py check`, `python manage.py test`, serta pengujian langsung melalui browser.