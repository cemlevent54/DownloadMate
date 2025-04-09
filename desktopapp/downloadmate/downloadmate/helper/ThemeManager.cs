using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public static class ThemeManager
    {
        public static string CurrentTheme { get; private set; } = "Light";

        public static void SetTheme(string theme)
        {
            CurrentTheme = theme;
        }

        public static void ApplyTheme(Control control)
        {
            if (CurrentTheme == "Dark")
            {
                control.BackColor = Color.Black;
                control.ForeColor = Color.White;
                foreach (Control c in control.Controls)
                    ApplyTheme(c);
            }
            else
            {
                control.BackColor = Color.White;
                control.ForeColor = Color.Black;
                foreach (Control c in control.Controls)
                    ApplyTheme(c);
            }
        }
    }
}
