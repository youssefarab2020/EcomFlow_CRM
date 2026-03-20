from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True)
    target_audience = models.CharField(max_length=255, help_text="مثلاً: أصحاب المحلات، النساء المهتمات بالجمال")
    benefits = models.TextField(help_text="شنو هي الفوائد الأساسية؟")
    problem_solved = models.TextField(help_text="شنو هو المشكل اللي كيهني منو العميل؟")
    
    # حقول الذكاء الاصطناعي (Smart AI Context)
    common_objections = models.TextField(blank=True, help_text="الاعتراضات (الثمن غالي، التوصيل...) وردودها")
    faq_context = models.TextField(blank=True, help_text="معلومات تقنية (الضمان، مدة التوصيل، طرق الدفع)")

    def __str__(self):
        return self.name