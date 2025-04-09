using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public class SettingsModel
    {
        public string Theme { get; set; } = "Light";  // Default değer
        public string Language { get; set; } = "en";  // İleride kullanılmak üzere
    }
}
