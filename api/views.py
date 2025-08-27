from django.shortcuts import render
import os
import tempfile
import uuid
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import yt_dlp
import json
import warnings

DOWNLOAD_DIR = tempfile.gettempdir()

warnings.filterwarnings("ignore", message=".*development server.*")

@csrf_exempt
@require_http_methods(["POST"])
def download_playlist(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        url = data.get("url")
        quality = data.get("quality", "1080")
        format_type = data.get("format", "mp4")

        if not url:
            return JsonResponse({"error": "Missing playlist URL"}, status=400)

        file_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

        ydl_opts = {
            "format": f"bestvideo[height<={quality}]+bestaudio/best/best",
            "outtmpl": output_template,
            "merge_output_format": format_type,
            "noplaylist": False,  # allow playlist
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                # For playlists, info["_type"] == "playlist" and info["entries"] is a list
                # We'll zip the playlist into a single file for download
                import zipfile
                zip_path = os.path.join(DOWNLOAD_DIR, f"{file_id}_playlist.zip")
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for entry in info.get("entries", []):
                        filename = ydl.prepare_filename(entry)
                        final_file = os.path.splitext(filename)[0] + f".{format_type}"
                        if os.path.exists(final_file):
                            zipf.write(final_file, os.path.basename(final_file))
                return FileResponse(open(zip_path, "rb"), as_attachment=True, filename=os.path.basename(zip_path))
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def download_facebook(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        url = data.get("url")
        quality = data.get("quality", "1080")
        format_type = data.get("format", "mp4")

        if not url:
            return JsonResponse({"error": "Missing Facebook video URL"}, status=400)

        file_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

        ydl_opts = {
            "format": f"bestvideo[height<={quality}]+bestaudio/best/best",
            "outtmpl": output_template,
            "merge_output_format": format_type,
            "noplaylist": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                final_file = os.path.splitext(filename)[0] + f".{format_type}"
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return FileResponse(open(final_file, "rb"), as_attachment=True, filename=os.path.basename(final_file))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
from django.shortcuts import render
import os
import tempfile
import uuid
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import yt_dlp
import json
import warnings


DOWNLOAD_DIR = tempfile.gettempdir()

warnings.filterwarnings("ignore", message=".*development server.*")


def downloader_ui(request):
    return render(request, "downloader.html")


@csrf_exempt
@require_http_methods(["POST"])
def download_video(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        url = data.get("url")
        quality = data.get("quality", "1080")
        format_type = data.get("format", "mp4")

        if not url:
            return JsonResponse({"error": "Missing video URL"}, status=400)

        file_id = str(uuid.uuid4())
        output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

        ydl_opts = {
            "format": f"bestvideo[height<={quality}]+bestaudio/best/best",
            "outtmpl": output_template,
            "merge_output_format": format_type,
            "noplaylist": True,
        }


        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                final_file = os.path.splitext(filename)[0] + f".{format_type}"
        except yt_dlp.utils.DownloadError as e:
            # If requested format is not available, return available formats
            try:
                with yt_dlp.YoutubeDL({"outtmpl": output_template, "noplaylist": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get("formats", [])
                    available = [
                        {
                            "format_id": f.get("format_id"),
                            "ext": f.get("ext"),
                            "height": f.get("height"),
                            "format_note": f.get("format_note"),
                            "filesize": f.get("filesize")
                        }
                        for f in formats if f.get("ext") in ["mp4", "webm", "mp3"]
                    ]
                return JsonResponse({
                    "error": "Requested format is not available.",
                    "available_formats": available
                }, status=400)
            except Exception as e2:
                return JsonResponse({"error": f"Requested format is not available. Could not fetch available formats. Details: {str(e2)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return FileResponse(open(final_file, "rb"), as_attachment=True, filename=os.path.basename(final_file))

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def video_info(request):
    url = request.GET.get("url")
    if not url:
        return JsonResponse({"error": "Missing video URL"}, status=400)

    try:
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)

        return JsonResponse({
            "title": info.get("title"),
            "duration": info.get("duration"),
            "views": info.get("view_count"),
            "channel": info.get("uploader"),
            "thumbnail": info.get("thumbnail"),
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
