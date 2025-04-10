using downloadmate.api;
using downloadmate.helper;
using downloadmate.webview;

namespace downloadmate
{
    public partial class main : Form
    {
        public main()
        {
            var settings = SettingsManager.Load();
            LanguageHelper.SetLanguage(settings.Language); // ?? Ýlk olarak burada çaðrýlmalý
            InitializeComponent();
            ThemeHelper.ApplyTheme(this, ThemeHelper.CurrentTheme);
            FormHelper.SetupForm(this);
        }

        private void btnSettings_Click(object sender, EventArgs e)
        {
            gotoSettingsPage();
        }

        private void main_Load(object sender, EventArgs e)
        {
            InitializeUI();
        }

        private async void btnDownload_ClickAsync(object sender, EventArgs e)
        {
            await HandleDownload();
        }

        private void btnOpenDownloads_Click(object sender, EventArgs e)
        {
            OpenDownloadFolder();
        }

        private void main_Activated(object sender, EventArgs e)
        {
            ApplySettings();
        }

        private void pctrBoxSettings_Click(object sender, EventArgs e)
        {
            gotoSettingsPage();
        }

        public void gotoSettingsPage()
        {
            settings settingsPage = new settings(this);
            settingsPage.Show();
            this.Hide();
        }

        public void setupCombobox()
        {
            List<string> options = new List<string>()
            {
                LanguageHelper.GetString("SelectOption"), // "Seçiniz" / "Select"
                LanguageHelper.GetString("Audio"),
                LanguageHelper.GetString("Video"), 
            };

            cmbBoxType.DataSource = options;

            cmbBoxType.SelectedIndex = 0;
        }

        private void InitializeUI()
        {
            setupCombobox();

            this.BeginInvoke(new Action(() =>
            {
                var settings = SettingsManager.Load();
                LanguageHelper.SetLanguage(settings.Language);

                if (Enum.TryParse(settings.Theme, out AppTheme theme))
                {
                    ThemeHelper.ApplyTheme(this, theme);
                    ThemeHelper.CurrentTheme = theme; // ?? Gerekli
                }



                lbType.Text = LanguageHelper.GetString("Type");
                lblUrl.Text = LanguageHelper.GetString("InputUrl");
                lblRename.Text = LanguageHelper.GetString("RenameFile");
                btnDownload.Text = LanguageHelper.GetString("Download");
                btnSettings.Text = LanguageHelper.GetString("Settings");
                btnOpenDownloads.Text = LanguageHelper.GetString("OpenDownloads");
            }));
        }

        private async Task HandleDownload()
        {
            string url = txtBoxUrl.Text.Trim();
            string type = cmbBoxType.SelectedItem.ToString();
            string fileName = txtBoxFileRename.Text.Trim();

            var cookies = GlobalCookies.LoadYouTubeCookies();

            var client = new DownloaderClient();
            try
            {
                string filePath = await client.DownloadFileAsync("youtube", url, type, cookies, fileName);
                MessageBox.Show($"{LanguageHelper.GetString("DownloadCompleted")}\n{filePath}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"{LanguageHelper.GetString("ErrorOccurred")} {ex.Message}");
            }
        }

        private void OpenDownloadFolder()
        {
            string folderPath = helper.DownloadPathHelper.GetDownloadDirectory();

            if (Directory.Exists(folderPath))
            {
                System.Diagnostics.Process.Start("explorer.exe", folderPath);
            }
            else
            {
                MessageBox.Show(LanguageHelper.GetString("DownloadFolderMissing"));
            }
        }


        private void ApplySettings()
        {
            var settings = SettingsManager.Load();
            LanguageHelper.SetLanguage(settings.Language);

            if (Enum.TryParse(settings.Theme, out AppTheme theme))
            {
                ThemeHelper.ApplyTheme(this, theme);
                ThemeHelper.CurrentTheme = theme;
            }

            UpdateLabels();
            setupCombobox();
        }

        private void UpdateLabels()
        {
            lbType.Text = LanguageHelper.GetString("Type");
            lblUrl.Text = LanguageHelper.GetString("InputUrl");
            lblRename.Text = LanguageHelper.GetString("RenameFile");
            btnDownload.Text = LanguageHelper.GetString("Download");
            btnSettings.Text = LanguageHelper.GetString("Settings");
            btnOpenDownloads.Text = LanguageHelper.GetString("OpenDownloads");
            lblHeader.Text = LanguageHelper.GetString("Title");
            this.Text = LanguageHelper.GetString("Main");
        }


        public void RefreshUI()
        {
            var settings = SettingsManager.Load();

            LanguageHelper.SetLanguage(settings.Language);

            if (Enum.TryParse(settings.Theme, out AppTheme theme))
            {
                ThemeHelper.ApplyTheme(this, theme);
                ThemeHelper.CurrentTheme = theme;
            }

            lbType.Text = LanguageHelper.GetString("Type");
            lblUrl.Text = LanguageHelper.GetString("InputUrl");
            lblRename.Text = LanguageHelper.GetString("RenameFile");
            btnDownload.Text = LanguageHelper.GetString("Download");
            btnSettings.Text = LanguageHelper.GetString("Settings");
            btnOpenDownloads.Text = LanguageHelper.GetString("OpenDownloads");

            setupCombobox();
        }

        
    }
}
