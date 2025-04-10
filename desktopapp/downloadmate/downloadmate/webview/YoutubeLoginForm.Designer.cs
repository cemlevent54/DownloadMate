namespace downloadmate.webview
{
    partial class YoutubeLoginForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;
        private Microsoft.Web.WebView2.WinForms.WebView2 webView;
        private System.Windows.Forms.Button btnExtractCookies;

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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(YoutubeLoginForm));
            webView = new Microsoft.Web.WebView2.WinForms.WebView2();
            btnExtractCookies = new Button();
            ((System.ComponentModel.ISupportInitialize)webView).BeginInit();
            SuspendLayout();
            // 
            // webView
            // 
            webView.AllowExternalDrop = true;
            webView.CreationProperties = null;
            webView.DefaultBackgroundColor = Color.White;
            webView.Location = new Point(12, 15);
            webView.Margin = new Padding(3, 4, 3, 4);
            webView.Name = "webView";
            webView.Size = new Size(572, 475);
            webView.TabIndex = 0;
            webView.ZoomFactor = 1D;
            // 
            // btnExtractCookies
            // 
            btnExtractCookies.Location = new Point(12, 500);
            btnExtractCookies.Margin = new Padding(3, 4, 3, 4);
            btnExtractCookies.Name = "btnExtractCookies";
            btnExtractCookies.Size = new Size(150, 44);
            btnExtractCookies.TabIndex = 1;
            btnExtractCookies.Text = "Çerezleri Al";
            btnExtractCookies.UseVisualStyleBackColor = true;
            btnExtractCookies.Click += btnExtractCookies_Click;
            // 
            // YoutubeLoginForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(596, 641);
            Controls.Add(btnExtractCookies);
            Controls.Add(webView);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Margin = new Padding(3, 4, 3, 4);
            Name = "YoutubeLoginForm";
            Text = "YouTube Giriş Yap";
            ((System.ComponentModel.ISupportInitialize)webView).EndInit();
            ResumeLayout(false);
        }

        #endregion
    }
}