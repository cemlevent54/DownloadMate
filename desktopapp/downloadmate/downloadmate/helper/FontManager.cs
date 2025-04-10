using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public static class FontManager
    {
        public static Font CurrentFont { get; private set; } = new Font("Lucida Calligraphy", 12F, FontStyle.Regular);

        public static void ApplyFont(Control control)
        {
            control.Font = CurrentFont;

            foreach (Control child in control.Controls)
            {
                ApplyFont(child); // recursive
            }
        }

    }
}
