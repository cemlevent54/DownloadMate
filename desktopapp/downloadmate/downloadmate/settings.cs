using downloadmate.helper;
using downloadmate.webview;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace downloadmate
{
    public partial class settings : Form
    {
        public settings(Form callingForm)
        {
            InitializeComponent();

            previousForm = callingForm;

            FormHelper.SetupForm(this);
        }

        private Form previousForm;



        private void btnBack_Click(object sender, EventArgs e)
        {
            gotoBack();
        }

        private void btnYoutube_Click(object sender, EventArgs e)
        {
            HandleYoutubeLogin();
        }

        private void cmbBoxSelectLanguage_SelectedIndexChanged(object sender, EventArgs e)
        {
            ApplySelectedLanguage();
        }

        private void btnInstagram_Click(object sender, EventArgs e)
        {
            HandleInstagramLogin();
        }

        private void btnTwitter_Click(object sender, EventArgs e)
        {
            HandleTwitterLogin();
        }

        private void btnOpenDownloads_Click(object sender, EventArgs e)
        {
            OpenDownloadFolder();
        }

        private void settings_Load(object sender, EventArgs e)
        {
            LoadSettings();
        }
        private void cmbBoxSelectTheme_SelectedIndexChanged(object sender, EventArgs e)
        {
            ApplySelectedTheme();
        }

        private void LoadSettings()
        {
            var settings = SettingsManager.Load();

            // Tema combobox'ına enum değerlerini ekle
            cmbBoxSelectTheme.Items.Clear();
            cmbBoxSelectTheme.Items.AddRange(Enum.GetNames(typeof(AppTheme)));
            if (Enum.TryParse<AppTheme>(settings.Theme, out var theme))
            {
                ThemeHelper.ApplyTheme(this, theme);
                cmbBoxSelectTheme.SelectedItem = settings.Theme;
            }

            // Kaydedilmiş tema varsa uygula
            cmbBoxSelectLanguage.Items.Clear();
            cmbBoxSelectLanguage.Items.Add("tr");
            cmbBoxSelectLanguage.Items.Add("en");
            cmbBoxSelectLanguage.SelectedItem = settings.Language ?? "tr";

            ApplyLocalization();
        }

        private void HandleYoutubeLogin()
        {
            YoutubeLoginForm form = new YoutubeLoginForm();
            if (form.ShowDialog() == DialogResult.OK)
            {
                string rawCookieString = form.CookieString;

                //  Filtrele
                string filtered = helper.CookieHelper.FilterYoutubeCookies(rawCookieString);

                //  Kalıcı kaydet
                GlobalCookies.SaveYouTubeCookies(filtered);

                MessageBox.Show(LanguageHelper.GetString("CookiesSaved"));
            }
        }

        private void HandleInstagramLogin()
        {
            InstagramLoginForm form = new InstagramLoginForm();
            if (form.ShowDialog() == DialogResult.OK)
            {
                string rawCookie = form.CookieString;
                string filtered = helper.CookieHelper.FilterInstagramCookies(rawCookie);

                GlobalCookies.SaveInstagramCookies(filtered);
                MessageBox.Show(LanguageHelper.GetString("CookiesSavedInstagram"));
            }
        }

        private void HandleTwitterLogin()
        {
            TwitterLoginForm form = new TwitterLoginForm();
            if (form.ShowDialog() == DialogResult.OK)
            {
                string rawCookieString = form.CookieString;

                // Çerezleri kaydet
                string filtered = helper.CookieHelper.FilterTwitterCookies(rawCookieString);
                GlobalCookies.SaveTwitterCookies(filtered);

                MessageBox.Show(LanguageHelper.GetString("CookiesSavedTwitter"));
            }
        }

        private void OpenDownloadFolder()
        {
            string folderPath = helper.DownloadPathHelper.GetDownloadDirectory();
            if (Directory.Exists(folderPath))
            {
                Process.Start("explorer.exe", folderPath);
            }
            else
            {
                MessageBox.Show(LanguageHelper.GetString("DownloadFolderMissing"));
            }
        }

        private void ApplyLocalization()
        {
            lblSelectLanguage.Text = LanguageHelper.GetString("SelectLanguage");
            lblSelectTheme.Text = LanguageHelper.GetString("SelectTheme");
            lblOpenDownloads.Text = LanguageHelper.GetString("OpenDownloads");
            btnBack.Text = LanguageHelper.GetString("Back");
            btnYoutube.Text = LanguageHelper.GetString("YoutubeLogin");
            btnInstagram.Text = LanguageHelper.GetString("InstagramLogin");
            btnOpenDownloads.Text = LanguageHelper.GetString("OpenDownloads");
            lblSettings.Text = LanguageHelper.GetString("Settings");
            this.Text = LanguageHelper.GetString("Settings");
        }

        private void ApplySelectedTheme()
        {
            string selectedTheme = cmbBoxSelectTheme.SelectedItem?.ToString() ?? "Light";

            if (Enum.TryParse<AppTheme>(selectedTheme, out var theme))
            {
                ThemeHelper.ApplyTheme(this, theme);
                ThemeHelper.CurrentTheme = theme;

                var settings = SettingsManager.Load();
                settings.Theme = selectedTheme;
                SettingsManager.Save(settings);
            }
        }

        private void ApplySelectedLanguage()
        {
            string selectedLang = cmbBoxSelectLanguage.SelectedItem?.ToString() ?? "tr";
            LanguageHelper.SetLanguage(selectedLang);

            var settings = SettingsManager.Load();
            settings.Language = selectedLang;
            SettingsManager.Save(settings);

            ApplyLocalization();
        }

        public void gotoBack()
        {
            var settings = SettingsManager.Load();

            // Tema ve dil uygula
            LanguageHelper.SetLanguage(settings.Language);

            if (previousForm is main mainForm)
            {
                // Tema ayarını da yükle
                if (Enum.TryParse(settings.Theme, out AppTheme theme))
                {
                    ThemeHelper.ApplyTheme(mainForm, theme);
                    ThemeHelper.CurrentTheme = theme;
                }

                // UI elemanlarını güncelle
                mainForm.RefreshUI();
            }

            previousForm.Show();
            this.Close();
        }

        
    }
}
