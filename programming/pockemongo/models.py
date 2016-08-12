from django.db import models


class Trainer(models.Model):
    '트레이너'
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # return self.name
        return 'Trainer#{} - {}'.format(self.id, self.name)


class Region(models.Model):
    '포획 지역'
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Pokemon(models.Model):
    '포켓몬'
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Capture(models.Model):
    '포획'
    trainer = models.ForeignKey(Trainer)
    pokemon = models.ForeignKey(Pokemon)
    region = models.ForeignKey(Region)
    location = models.CharField(max_length=100, verbose_name='포획위치 설명')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}가 {}를 {}의 {}에서 포획'.format(self.trainer.name, self.pokemon.name, self.region.name, self.location)
