using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http.Headers;
using System.Threading;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UploadController : Controller
    {
        [HttpPost("UploadMapImage", Name = "UploadFile")]

        public async Task<IActionResult> UploadFile()
        {
            var files = HttpContext.Request.Form.Files;
            if (files.Count > 0)
                if (CheckIfImageFile(files[0]))
                {
                    var res = await WriteFile(files[0]);

                    return Ok(new { message = res });
                }
                else
                {
                    return BadRequest(new { message = "Invalid file extension" });
                }

            // return Ok();
            else
            {
                return BadRequest(new { message = "Please Upload a file" });
            }
        }

        private bool CheckIfImageFile(IFormFile file)
        {
            var extension = "." + file.FileName.Split('.')[file.FileName.Split('.').Length - 1].ToLower();
            return (extension == ".png" || extension == ".jpg" || extension == ".jpeg"); // Change the extension based on your need
        }

        private async Task<String> WriteFile(IFormFile file)
        {
            string fileName;
            try
            {
                var extension = "." + file.FileName.Split('.')[file.FileName.Split('.').Length - 1];
                fileName = "Map1.jpg"; //+ extension; //Create a new Name for the file due to security reasons.

                var pathBuilt = Path.Combine(Directory.GetCurrentDirectory(), "Resources\\Images");

                if (!Directory.Exists(pathBuilt))
                {
                    Directory.CreateDirectory(pathBuilt);
                }

                var path = Path.Combine(Directory.GetCurrentDirectory(), "Resources\\Images",
                   fileName);

                using (var stream = new FileStream(path, FileMode.Create))
                {
                    await file.CopyToAsync(stream);
                }

                return "/Resources/Images/Map1.jpg";
            }
            catch (Exception e)
            {
                return e.Message;
            }
        }
    }
}
