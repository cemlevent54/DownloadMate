namespace downloadmate
{
    partial class settings
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(settings));
            lblSettings = new Label();
            btnBack = new Button();
            lblSelectLanguage = new Label();
            lblSelectTheme = new Label();
            label1 = new Label();
            btnInstagram = new Button();
            btnYoutube = new Button();
            lblOpenDownloads = new Label();
            btnOpenDownloads = new Button();
            cmbBoxSelectLanguage = new ComboBox();
            cmbBoxSelectTheme = new ComboBox();
            SuspendLayout();
            // 
            // lblSettings
            // 
            lblSettings.Location = new Point(230, 34);
            lblSettings.Name = "lblSettings";
            lblSettings.Size = new Size(200, 30);
            lblSettings.TabIndex = 16;
            lblSettings.Text = "Settings";
            lblSettings.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // btnBack
            // 
            btnBack.Location = new Point(32, 34);
            btnBack.Name = "btnBack";
            btnBack.Size = new Size(100, 35);
            btnBack.TabIndex = 1;
            btnBack.Text = "Back";
            btnBack.UseVisualStyleBackColor = true;
            btnBack.Click += btnBack_Click;
            // 
            // lblSelectLanguage
            // 
            lblSelectLanguage.Location = new Point(32, 110);
            lblSelectLanguage.Name = "lblSelectLanguage";
            lblSelectLanguage.Size = new Size(200, 35);
            lblSelectLanguage.TabIndex = 15;
            lblSelectLanguage.Text = "Select Language:";
            lblSelectLanguage.TextAlign = ContentAlignment.MiddleRight;
            // 
            // lblSelectTheme
            // 
            lblSelectTheme.Location = new Point(32, 170);
            lblSelectTheme.Name = "lblSelectTheme";
            lblSelectTheme.Size = new Size(200, 35);
            lblSelectTheme.TabIndex = 14;
            lblSelectTheme.Text = "Select Theme:";
            lblSelectTheme.TextAlign = ContentAlignment.MiddleRight;
            // 
            // label1
            // 
            label1.Location = new Point(32, 240);
            label1.Name = "label1";
            label1.Size = new Size(200, 35);
            label1.TabIndex = 13;
            label1.Text = "Social Media Login:";
            label1.TextAlign = ContentAlignment.MiddleRight;
            // 
            // btnInstagram
            // 
            btnInstagram.Location = new Point(250, 240);
            btnInstagram.Name = "btnInstagram";
            btnInstagram.Size = new Size(154, 38);
            btnInstagram.TabIndex = 5;
            btnInstagram.Text = "Instagram";
            btnInstagram.UseVisualStyleBackColor = true;
            btnInstagram.Click += btnInstagram_Click;
            // 
            // btnYoutube
            // 
            btnYoutube.Location = new Point(421, 240);
            btnYoutube.Name = "btnYoutube";
            btnYoutube.Size = new Size(151, 38);
            btnYoutube.TabIndex = 6;
            btnYoutube.Text = "Youtube";
            btnYoutube.UseVisualStyleBackColor = true;
            btnYoutube.Click += btnYoutube_Click;
            // 
            // lblOpenDownloads
            // 
            lblOpenDownloads.Location = new Point(32, 320);
            lblOpenDownloads.Name = "lblOpenDownloads";
            lblOpenDownloads.Size = new Size(200, 35);
            lblOpenDownloads.TabIndex = 12;
            lblOpenDownloads.Text = "Open Downloads:";
            lblOpenDownloads.TextAlign = ContentAlignment.MiddleRight;
            // 
            // btnOpenDownloads
            // 
            btnOpenDownloads.Location = new Point(250, 320);
            btnOpenDownloads.MinimumSize = new Size(120, 0);
            btnOpenDownloads.Name = "btnOpenDownloads";
            btnOpenDownloads.Size = new Size(140, 38);
            btnOpenDownloads.TabIndex = 9;
            btnOpenDownloads.Text = "Open";
            btnOpenDownloads.UseVisualStyleBackColor = true;
            btnOpenDownloads.Click += btnOpenDownloads_Click;
            // 
            // cmbBoxSelectLanguage
            // 
            cmbBoxSelectLanguage.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbBoxSelectLanguage.DropDownWidth = 250;
            cmbBoxSelectLanguage.FormattingEnabled = true;
            cmbBoxSelectLanguage.Location = new Point(250, 110);
            cmbBoxSelectLanguage.Name = "cmbBoxSelectLanguage";
            cmbBoxSelectLanguage.Size = new Size(200, 31);
            cmbBoxSelectLanguage.TabIndex = 10;
            cmbBoxSelectLanguage.SelectedIndexChanged += cmbBoxSelectLanguage_SelectedIndexChanged;
            // 
            // cmbBoxSelectTheme
            // 
            cmbBoxSelectTheme.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbBoxSelectTheme.FormattingEnabled = true;
            cmbBoxSelectTheme.Location = new Point(250, 170);
            cmbBoxSelectTheme.Name = "cmbBoxSelectTheme";
            cmbBoxSelectTheme.Size = new Size(200, 31);
            cmbBoxSelectTheme.TabIndex = 11;
            cmbBoxSelectTheme.SelectedIndexChanged += cmbBoxSelectTheme_SelectedIndexChanged;
            // 
            // settings
            // 
            AutoScaleDimensions = new SizeF(9F, 23F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(600, 450);
            Controls.Add(cmbBoxSelectTheme);
            Controls.Add(cmbBoxSelectLanguage);
            Controls.Add(btnOpenDownloads);
            Controls.Add(lblOpenDownloads);
            Controls.Add(btnYoutube);
            Controls.Add(btnInstagram);
            Controls.Add(label1);
            Controls.Add(lblSelectTheme);
            Controls.Add(lblSelectLanguage);
            Controls.Add(btnBack);
            Controls.Add(lblSettings);
            Font = new Font("Segoe UI", 10F);
            FormBorderStyle = FormBorderStyle.FixedSingle;
            Icon = (Icon)resources.GetObject("$this.Icon");
            MaximizeBox = false;
            Name = "settings";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Settings";
            Load += settings_Load;
            ResumeLayout(false);
        }

        #endregion

        private Label lblSettings;
        private Button btnBack;
        private Label lblSelectLanguage;
        private Label lblSelectTheme;
        private Label label1;
        private Button btnInstagram;
        private Button btnYoutube;
        private Label lblOpenDownloads;
        private Button btnOpenDownloads;
        private ComboBox cmbBoxSelectLanguage;
        private ComboBox cmbBoxSelectTheme;
    }
}