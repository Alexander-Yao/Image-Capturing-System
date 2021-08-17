using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Threading.Tasks;

namespace MapsVisionsAPI.Data.Entities
{
    //[Keyless]
    public class MapImageRecogResults
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]

        public int capture_id { set; get; }
        public float lng { get; set; }
        public float lat { get; set; }
        public string map_provider { get; set; }
        public int zoom_level { get; set; }
        public string capture_url { get; set; }
        public string quarter { get; set; }
        public string effects { get; set; }
        public float confidence { get; set; }
        public float matching_degree { get; set; }
        public int no_detected_words { get; set; }
        public int no_undetected_words { get; set; }
        public int no_wrong_words { get; set; }
        public float total_matching_degree { get; set; }
    }
}
