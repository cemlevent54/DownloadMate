using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace downloadmate.helper
{
    public static class DownloadPathHelper
    {
        public static string GetDownloadDirectory()
        {
            var downloadsFolder = Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),
                "Downloads",
                "DownloadMateDownloads"
            );

            if (!Directory.Exists(downloadsFolder))
            {
                Directory.CreateDirectory(downloadsFolder);
            }

            return downloadsFolder;
        }

        public static string GetFilePath(string filename)
        {
            return Path.Combine(GetDownloadDirectory(), filename);
        }
    }
}
