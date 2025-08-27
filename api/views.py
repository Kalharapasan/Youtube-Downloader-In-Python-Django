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
            # Try fallback to 'best' if requested format is not available
            fallback_opts = ydl_opts.copy()
            fallback_opts["format"] = "best"
            try:
                with yt_dlp.YoutubeDL(fallback_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    final_file = os.path.splitext(filename)[0] + f".{format_type}"
            except Exception as e2:
                return JsonResponse({"error": f"Requested format is not available. Try a different quality or format. Details: {str(e2)}"}, status=400)
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
