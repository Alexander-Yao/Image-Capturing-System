using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using Tesseract;

namespace MapsVisionsAPI.Middleware
{
    public class TesseractReading
    {
        public void TesseractReader(string imagePath,out float confidence, out string text, out string csvText)
        {
            try
            {
                var tessDataFolder = Path.Combine(Directory.GetCurrentDirectory(), "tessdata");
                var engine = new TesseractEngine(tessDataFolder, "eng", EngineMode.Default);
                Bitmap mapImg = new Bitmap(imagePath);
                var pix = Tesseract.Pix.LoadFromFile(imagePath);
                var page = engine.Process(pix);
                text = page.GetText();
                csvText = page.GetTsvText(0);
                confidence = page.GetMeanConfidence();
            }catch(Exception ex)
            {
                text = "";
                csvText = "";
                confidence = 0f;
            }
        }
    }
}
