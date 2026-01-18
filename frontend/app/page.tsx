import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navbar */}
      <nav className="bg-white border-b border-secondary-200">
        <div className="container-custom">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-primary">Diyetisyen</span>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/login" className="text-secondary-700 hover:text-primary transition-colors">
                Giriş Yap
              </Link>
              <Link href="/register" className="btn-primary">
                Üye Ol
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 bg-gradient-to-b from-primary-50 to-white">
        <div className="container-custom">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold text-secondary-900 mb-6">
              Sağlıklı Yaşam İçin
              <span className="text-primary"> Profesyonel Destek</span>
            </h1>
            <p className="text-xl text-secondary-600 mb-8 max-w-2xl mx-auto">
              Uzman diyetisyenlerimizle kişiselleştirilmiş beslenme programları oluşturun, ilerlemenizi takip edin ve hedeflerinize ulaşın.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/register" className="btn-primary text-lg px-8 py-3">
                Hemen Başla
              </Link>
              <Link href="#services" className="btn-outline text-lg px-8 py-3">
                Hizmetlerimiz
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="services" className="py-20">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">Hizmetlerimiz</h2>
            <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
              Modern ve kullanıcı dostu platformumuzla beslenme hedeflerinize kolay yoldan ulaşın
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="card hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-2">Online Randevu</h3>
              <p className="text-secondary-600">
                Diyetisyenlerinizle kolayca randevu alın ve online görüşmeler yapın
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-2">Kişisel Diyet Planı</h3>
              <p className="text-secondary-600">
                Size özel hazırlanmış beslenme programları ve öğün planları
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-2">İlerleme Takibi</h3>
              <p className="text-secondary-600">
                Kilo ve vücut ölçümlerinizi kaydedin, grafiklerle ilerlemenizi görün
              </p>
            </div>

            <div className="card hover:shadow-lg transition-shadow">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-secondary-900 mb-2">Beslenme Blogu</h3>
              <p className="text-secondary-600">
                Sağlıklı yaşam ve beslenme hakkında güncel bilgiler ve tarifler
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-50">
        <div className="container-custom">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-secondary-900 mb-4">
              Sağlıklı Yaşam Yolculuğunuza Bugün Başlayın
            </h2>
            <p className="text-lg text-secondary-600 mb-8">
              Uzman diyetisyenlerimiz sizin için hazır. Hemen üye olun ve kişiselleştirilmiş beslenme desteği alın.
            </p>
            <Link href="/register" className="btn-primary text-lg px-8 py-3 inline-block">
              Ücretsiz Üye Ol
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-secondary-900 text-white py-12">
        <div className="container-custom">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-primary mb-4">Diyetisyen</h3>
              <p className="text-secondary-300">
                Sağlıklı yaşam için profesyonel beslenme danışmanlığı
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Hızlı Linkler</h4>
              <ul className="space-y-2">
                <li><Link href="/about" className="text-secondary-300 hover:text-primary transition-colors">Hakkımızda</Link></li>
                <li><Link href="/blog" className="text-secondary-300 hover:text-primary transition-colors">Blog</Link></li>
                <li><Link href="/contact" className="text-secondary-300 hover:text-primary transition-colors">İletişim</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">İletişim</h4>
              <p className="text-secondary-300">
                E-posta: info@diyetisyen.com<br />
                Telefon: (0212) 555 0 555
              </p>
            </div>
          </div>
          <div className="border-t border-secondary-800 mt-8 pt-8 text-center text-secondary-400">
            <p>&copy; 2026 Diyetisyen. Tüm hakları saklıdır.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
