﻿using downloadmate.helper;

namespace downloadmate
{
    partial class main
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
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
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(main));
            txtBoxUrl = new TextBox();
            cmbBoxType = new ComboBox();
            txtBoxFileRename = new TextBox();
            btnDownload = new Button();
            btnOpenDownloads = new Button();
            lblUrl = new Label();
            lblHeader = new Label();
            lbType = new Label();
            lblRename = new Label();
            btnSettings = new Button();
            SuspendLayout();
            // 
            // txtBoxUrl
            // 
            txtBoxUrl.Font = new Font("Segoe UI", 12F);
            txtBoxUrl.Location = new Point(160, 80);
            txtBoxUrl.Name = "txtBoxUrl";
            txtBoxUrl.Size = new Size(400, 34);
            txtBoxUrl.TabIndex = 0;
            // 
            // cmbBoxType
            // 
            cmbBoxType.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbBoxType.Font = new Font("Segoe UI", 12F);
            cmbBoxType.FormattingEnabled = true;
            cmbBoxType.Location = new Point(160, 130);
            cmbBoxType.Name = "cmbBoxType";
            cmbBoxType.Size = new Size(250, 36);
            cmbBoxType.TabIndex = 1;
            // 
            // txtBoxFileRename
            // 
            txtBoxFileRename.Font = new Font("Segoe UI", 12F);
            txtBoxFileRename.Location = new Point(160, 180);
            txtBoxFileRename.Name = "txtBoxFileRename";
            txtBoxFileRename.Size = new Size(400, 34);
            txtBoxFileRename.TabIndex = 2;
            // 
            // btnDownload
            // 
            btnDownload.Font = new Font("Segoe UI", 10F);
            btnDownload.Location = new Point(230, 240);
            btnDownload.Name = "btnDownload";
            btnDownload.Size = new Size(130, 38);
            btnDownload.TabIndex = 3;
            btnDownload.Text = "Download";
            btnDownload.UseVisualStyleBackColor = true;
            btnDownload.Click += btnDownload_ClickAsync;
            // 
            // btnOpenDownloads
            // 
            btnOpenDownloads.Font = new Font("Segoe UI", 10F);
            btnOpenDownloads.Location = new Point(390, 410);
            btnOpenDownloads.Name = "btnOpenDownloads";
            btnOpenDownloads.Size = new Size(170, 45);
            btnOpenDownloads.TabIndex = 4;
            btnOpenDownloads.Text = "Open Downloads";
            btnOpenDownloads.UseVisualStyleBackColor = true;
            btnOpenDownloads.Click += btnOpenDownloads_Click;
            // 
            // lblUrl
            // 
            lblUrl.Location = new Point(10, 80);
            lblUrl.Name = "lblUrl";
            lblUrl.Size = new Size(140, 30);
            lblUrl.TabIndex = 13;
            lblUrl.Text = "Input URL:";
            lblUrl.TextAlign = ContentAlignment.MiddleRight;
            // 
            // lblHeader
            // 
            lblHeader.Font = new Font("Segoe UI", 13F, FontStyle.Bold);
            lblHeader.Location = new Point(100, 20);
            lblHeader.Name = "lblHeader";
            lblHeader.Size = new Size(400, 30);
            lblHeader.TabIndex = 12;
            lblHeader.Text = "DownloadMate Desktop App";
            lblHeader.TextAlign = ContentAlignment.MiddleCenter;
            // 
            // lbType
            // 
            lbType.Location = new Point(10, 130);
            lbType.Name = "lbType";
            lbType.Size = new Size(140, 30);
            lbType.TabIndex = 11;
            lbType.Text = "Type:";
            lbType.TextAlign = ContentAlignment.MiddleRight;
            // 
            // lblRename
            // 
            lblRename.Location = new Point(10, 180);
            lblRename.Name = "lblRename";
            lblRename.Size = new Size(140, 30);
            lblRename.TabIndex = 10;
            lblRename.Text = "Rename File:";
            lblRename.TextAlign = ContentAlignment.MiddleRight;
            // 
            // btnSettings
            // 
            btnSettings.Font = new Font("Segoe UI", 10F);
            btnSettings.Location = new Point(69, 410);
            btnSettings.Name = "btnSettings";
            btnSettings.Size = new Size(130, 45);
            btnSettings.TabIndex = 9;
            btnSettings.Text = "Settings";
            btnSettings.UseVisualStyleBackColor = true;
            btnSettings.Click += btnSettings_Click;
            // 
            // main
            // 
            AutoScaleDimensions = new SizeF(9F, 23F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(600, 550);
            Controls.Add(btnOpenDownloads);
            Controls.Add(btnSettings);
            Controls.Add(lblRename);
            Controls.Add(lbType);
            Controls.Add(lblHeader);
            Controls.Add(lblUrl);
            Controls.Add(btnDownload);
            Controls.Add(txtBoxFileRename);
            Controls.Add(cmbBoxType);
            Controls.Add(txtBoxUrl);
            Font = new Font("Segoe UI", 10F);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "main";
            Text = "Main";
            Activated += main_Activated;
            Load += main_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private TextBox txtBoxUrl;
        private ComboBox cmbBoxType;
        private TextBox txtBoxFileRename;
        private Button btnDownload;
        private Button btnOpenDownloads;
        private Label lblUrl;
        private Label lblHeader;
        private Label lbType;
        private Label lblRename;
        private Button btnSettings;
    }
}
