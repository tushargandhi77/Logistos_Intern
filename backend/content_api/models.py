from django.db import models

class Content(models.Model):
    CONTENT_TYPES = (
        ('testimonial', 'Testimonial'),
        ('testcase', 'Test Case'),
        ('blog', 'Blog'),
    )
    
    type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    content = models.TextField()

    def __str__(self):
        return f"{self.type} - {self.id}"
