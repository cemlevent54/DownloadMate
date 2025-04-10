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
    public partial class InstagramLoginForm: Form
    {
        public string CookieString { get; private set; } = "";

        public InstagramLoginForm()
        {
            InitializeComponent();
            InitializeAsync();
            FormHelper.SetupForm(this);

            this.Text = LanguageHelper.GetString("InstagramLoginForm_Title");
            btnExtractCookies.Text = LanguageHelper.GetString("ExtractCookiesButton");
        }

        private async void btnExtractCookies_Click(object sender, EventArgs e)
        {
            extractCookies();
        }

        private async void InitializeAsync()
        {
            await webView.EnsureCoreWebView2Async(null);
            webView.CoreWebView2.Navigate("https://www.instagram.com/accounts/login/");
        }

        

        private async void extractCookies()
        {
            var cookieManager = webView.CoreWebView2.CookieManager;
            var cookies = await cookieManager.GetCookiesAsync("https://www.instagram.com");

            string[] requiredKeys = { "sessionid", "ds_user_id" };
            var filtered = cookies
                .Where(c => requiredKeys.Contains(c.Name))
                .Select(c => $"{c.Name}={c.Value}");

            CookieString = string.Join("; ", filtered);

            MessageBox.Show(LanguageHelper.GetString("InstagramCookiesSuccess"));
            this.DialogResult = DialogResult.OK;
            this.Close();
        }


    }
}
