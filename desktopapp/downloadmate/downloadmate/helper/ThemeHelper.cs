using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public enum AppTheme
    {
        Light,
        Dark
    }

    public static class ThemeHelper
    {
        public static AppTheme CurrentTheme { get; set; } = AppTheme.Light;

        public static void ApplyTheme(Form form, AppTheme theme)
        {
            CurrentTheme = theme;

            Color backColor = theme == AppTheme.Dark ? Color.FromArgb(30, 30, 30) : Color.White;
            Color foreColor = theme == AppTheme.Dark ? Color.White : Color.Black;

            form.BackColor = backColor;

            foreach (Control control in form.Controls)
            {
                control.ForeColor = foreColor;
                control.BackColor = (control is Button || control is ComboBox || control is TextBox)
                    ? Color.FromArgb(theme == AppTheme.Dark ? 45 : 255, theme == AppTheme.Dark ? 45 : 255, theme == AppTheme.Dark ? 45 : 255)
                    : backColor;
            }
        }
    }
}
