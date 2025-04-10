using downloadmate.helper;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace downloadmate.webview
{
    public partial class TwitterLoginForm : Form
    {
        public TwitterLoginForm()
        {
            InitializeComponent();
            InitializeAsync();
            FormHelper.SetupForm(this);

            this.Text = LanguageHelper.GetString("TwitterLoginForm_Title");
            btnExtractCookies.Text = LanguageHelper.GetString("ExtractCookiesButton");
        }

        public string CookieString { get; private set; }

        private async void btnExtractCookies_Click(object sender, EventArgs e)
        {
            extractCookies();
        }

        private async void InitializeAsync()
        {
            await webView.EnsureCoreWebView2Async(null);
            webView.CoreWebView2.Navigate("https://twitter.com/login"); // ✅ Burası olmalı
        }

        private async void extractCookies()
        {
            var cookieManager = webView.CoreWebView2.CookieManager;
            var cookies = await cookieManager.GetCookiesAsync("https://twitter.com");

            // Örnek olarak bazı yaygın cookie isimleri filtrelenebilir
            string[] requiredKeys = { "auth_token", "ct0", "guest_id" };

            var filtered = cookies
                .Where(c => requiredKeys.Contains(c.Name))
                .Select(c => $"{c.Name}={c.Value}");

            CookieString = string.Join("; ", filtered);

            MessageBox.Show(LanguageHelper.GetString("TwitterCookiesSuccess"));
            this.DialogResult = DialogResult.OK;
            this.Close();
        }

        
    }
}
