using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using OpenCvSharp;
using OpenCvSharp.Extensions;

namespace MapsVisionsAPI.Middleware
{
    public class ImageFilters
    {
        public static bool applyGrayscale(string imagePath)
        {            
            Mat Grayscale = Cv2.ImRead(imagePath, ImreadModes.Grayscale);
            return saveMatImage(Grayscale, "Grayscale1", imagePath);
        }
        private static bool saveMatImage(Mat img, string name, string sourcePath)
        {
            var imagePath = Path.Combine(sourcePath.Substring(0,sourcePath.LastIndexOf("\\")+1),
                   name +"-"+ sourcePath.Substring(sourcePath.LastIndexOf("\\")+1));
            Bitmap bitmap = BitmapConverter.ToBitmap(img);
            bitmap.Save(imagePath);
            return true;
        }

        public static bool applyBestEffects2(string imagePath)
        {
            Mat image = Cv2.ImRead(imagePath, ImreadModes.Unchanged);
           // Mat bestlabeled;
            //Cv2.Kmeans(image,20,bestlabeled,)

            // return saveMatImage(Grayscale, "Grayscale1", imagePath);
            return true;
        }

        public static bool applyBestEffects1(string imagePath)
        {
            Mat image = Cv2.ImRead(imagePath, ImreadModes.Unchanged);
            Mat grayImg=new Mat();
            Mat erosion = new Mat();
            Mat thresh = new Mat();
            Mat opening = new Mat();
            Mat dilate = new Mat();
            
            Cv2.CvtColor(image, grayImg, ColorConversionCodes.BGR2GRAY);

            //gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            Mat kernel = Cv2.GetStructuringElement(MorphShapes.Rect, new OpenCvSharp.Size(3, 3));

            Cv2.AdaptiveThreshold(grayImg, thresh, 255, AdaptiveThresholdTypes.MeanC, ThresholdTypes.Binary, 17,13);
            Cv2.Erode(grayImg, erosion, null, null, 1);
            Cv2.Dilate(grayImg, dilate, null,null,  1);
            // thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 3)

            // Morph open
            // kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            Cv2.MorphologyEx(thresh, opening, MorphTypes.Erode, kernel,null, 1);
            //opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)

            //Remove noise by filtering using contour area
            Mat[] contours;//= new Mat[]();
            Mat hierarchy = new Mat();
            Mat cnts = new Mat();
            Cv2.FindContours(opening, out contours, hierarchy, RetrievalModes.External, 
                ContourApproximationModes.ApproxSimple);
            //cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if (contours.Length == 2)
                cnts = contours[0];
            else
                cnts = contours[1];
            int x = 0;
            foreach(var c in contours)
            {

               // Mat img_contours = Cv2.
// draw the contours on the empty image
/*cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 3);

                saveMatImage(c, "contours"+x.ToString(), imagePath);
                x++;
                double area=  Cv2.ContourArea(c);
                if (area < 10)
                    Cv2.DrawContours(opening, new[] { c }, -1, Scalar.Black, -1);
            */}
            /*
            for c in cnts:
                area = cv2.contourArea(c)
                if area < 10:
                    cv2.drawContours(opening, [c], -1, (0, 0, 0), -1)
                */
            // Invert image for result
            Mat result = 255 - opening;
            saveMatImage(image, "normal", imagePath);
            saveMatImage(grayImg, "gray", imagePath);
            saveMatImage(dilate, "dilate", imagePath);
            saveMatImage(erosion, "erosion", imagePath);
            saveMatImage(thresh, "ThreshMeanCBinary", imagePath);
            saveMatImage(opening, "opening", imagePath);
            saveMatImage(result, "result", imagePath);
            return true;
        }


    }
}
