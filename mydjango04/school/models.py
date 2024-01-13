from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    student_set = models.ManyToManyField(
        to=Student,
        related_name="subject_set",
        related_query_name="subject",
        through="Enrollment",
        through_fields=("subject", "student"),
        blank=True,
    )

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    class Term(models.TextChoices):
        SPRING = "SP", "봄학기"
        SUMMER = "SU", "여름학기"
        FALL = "FA", "가을학기"
        WINTER = "WI", "겨울학기"

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollment_set",
        related_query_name="enrollment",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="enrollment_set",
        related_query_name="enrollment",
    )
    year = models.PositiveIntegerField(verbose_name="수강년도")
    term = models.CharField(max_length=2, choices=Term.choices, verbose_name="학기")
    is_pass = models.BooleanField(verbose_name="이수 여부", default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "year", "term"],
                name="school_enrollment_unique",
            )
        ]
