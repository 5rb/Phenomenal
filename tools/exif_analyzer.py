import os
import json
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

class AdvancedExifAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path
        self.report_data = {}

    def _convert_to_degrees(self, value):
        """Helper function to convert the GPS camera coordiantes to degrees."""
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)

    def extract_gps_info(self, exif_data):
        gps_info = {}
        if "GPSInfo" in exif_data:
            for key in exif_data["GPSInfo"].keys():
                decode_tag = GPSTAGS.get(key, key)
                gps_info[decode_tag] = exif_data["GPSInfo"][key]

            # Parse coordinates for Google Maps URL
            latitude = gps_info.get("GPSLatitude")
            latitude_ref = gps_info.get("GPSLatitudeRef")
            longitude = gps_info.get("GPSLongitude")
            longitude_ref = gps_info.get("GPSLongitudeRef")

            if latitude and latitude_ref and longitude and longitude_ref:
                lat = self._convert_to_degrees(latitude)
                if latitude_ref != "N":
                    lat = 0 - lat

                lon = self._convert_to_degrees(longitude)
                if longitude_ref != "E":
                    lon = 0 - lon
                
                maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                return {"lat": lat, "lon": lon, "google_maps_url": maps_url}
        return None

    def analyze(self):
        if not os.path.exists(self.image_path):
            print(f"[-] Error: File '{self.image_path}' not found.")
            return

        print(f"[*] Extracting forensic signatures from: {os.path.basename(self.image_path)}")
        try:
            with Image.open(self.image_path) as img:
                self.report_data["File Name"] = os.path.basename(self.image_path)
                self.report_data["Format"] = img.format
                self.report_data["Mode"] = img.mode
                self.report_data["Size"] = f"{img.width}x{img.height}"
                
                exif = img._getexif()
                if not exif:
                    print("[-] No detailed EXIF structural signatures embedded.")
                    return

                raw_exif = {}
                for tag, value in exif.items():
                    decoded = TAGS.get(tag, tag)
                    if isinstance(value, bytes):
                        value = value[:30] + b"..."  # Clean representation
                    raw_exif[str(decoded)] = str(value)
                
                self.report_data["EXIF_Data"] = raw_exif
                
                # Extract Geo-location data
                gps_data = self.extract_gps_info(raw_exif)
                if gps_data:
                    self.report_data["Spatial_Coordinates"] = gps_data
                    print(f"[+] GEO-LOCATION FOUND: {gps_data['google_maps_url']}")

                # Export structured JSON report
                output_file = f"report_{os.path.splitext(self.image_path)[0]}.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(self.report_data, f, indent=4, ensure_ascii=False)
                
                print(f"[+] Operational data dumped successfully into: {output_file}")
                print(json.dumps(self.report_data, indent=2))

        except Exception as e:
            print(f"[-] Forensic pipeline failure: {str(e)}")

if __name__ == "__main__":
    target_img = input("Enter operational path to target image: ").strip()
    analyzer = AdvancedExifAnalyzer(target_img)
    analyzer.analyze()
