from django.db import models

# import os
# import re


def logo_directory_path(instance, filename):
    # image_name = re.sub(r"[-\s]+", "_", re.sub(r"[^\w\s-]", "", instance.name.lower())).strip("-_")
    # _, extension = os.path.splitext(filename)
    # return f"Images/{image_name}{extension}"
    return "/".join(["Inputs", filename])


def output_path(instance, filename):
    # image_name = re.sub(r"[-\s]+", "_", re.sub(r"[^\w\s-]", "", instance.name.lower())).strip("-_")
    # _, extension = os.path.splitext(filename)
    # return f"Output/{image_name}_bg_removed{extension}"
    return "/".join(["Outputs", filename])


class Image(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=500, blank=True, null=True)
    picture = models.ImageField(upload_to=logo_directory_path, blank=True, null=True)
    nobg = models.ImageField(upload_to=output_path, blank=True, null=True)
