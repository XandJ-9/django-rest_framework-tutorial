from rest_framework import serializers 

from .models import Drone, DroneCategory, Competition, Pilot


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = serializers.HyperlinkedRelatedField(
    many=True,
    read_only=True,
    view_name='drone-detail')  # 指定字段访问的url视图名称

    

    class Meta:
        model = DroneCategory
        fields = '__all__'



class DroneSerializer(serializers.HyperlinkedModelSerializer):
    # Display the category name
    # 根据指定对象的 slug_field 字段来显示
    # 查找对象集合中name='xxx'的对象，并返回其slug值,默认返回主键值
    drone_category = serializers.SlugRelatedField(queryset=DroneCategory.objects.all(), slug_field='name')

    class Meta:
        model = Drone
        fields = '__all__'



class CompetitionSerializer(serializers.HyperlinkedModelSerializer):
    # Display all the details for the related drone
    drone = DroneSerializer()
    class Meta:
        model = Competition
        fields = (
        'url',
        'pk',
        'distance_in_feet',
        'distance_achievement_date',
        'drone')


class PilotSerializer(serializers.HyperlinkedModelSerializer):
    competitions = CompetitionSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Pilot.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display',read_only=True)

    class Meta:
        model = Pilot
        fields = (
        'url',
        'name',
        'gender',
        'gender_description',
        'races_count',
        'inserted_timestamp',
        'competitions')


class PilotCompetitionSerializer(serializers.ModelSerializer):
    # Display the pilot's name
    pilot = serializers.SlugRelatedField(queryset=Pilot.objects.all(),
    slug_field='name')
    # Display the drone's name
    drone = serializers.SlugRelatedField(queryset=Drone.objects.all(),
    slug_field='name')
    class Meta:
        model = Competition
        fields = (
        'url',
        'pk',
        'distance_in_feet',
        'distance_achievement_date',
        'pilot',
        'drone')