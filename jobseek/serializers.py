from rest_framework import serializers
from .models import Company, Job, JobSkill, Skill, CustomUser, Application

# Company serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'description', 'website', 'company_logo']

# Job serializer
class JobSerializer(serializers.ModelSerializer):
    #skills = serializers.StringRelatedField(many=True)
    company = serializers.StringRelatedField()
    #job_type = serializers.CharField(source='get_job_type_display')
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'company', 'location', 'job_type', 'experience_level', 'salary', 'is_active']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        

# JobSkill serializer
class JobSkillSerializer(serializers.ModelSerializer):
    skill = serializers.StringRelatedField(read_only = False)
    job = serializers.StringRelatedField()
    class Meta:
        model = JobSkill
        fields = ['id', 'job', 'skill']
        


# User serializer
class CustomUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'phone_number', 'dob', 'profile_picture', 'bio', 'address']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Ensure both passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')   
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Application serializer
class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant_name', 'applicant_email', 'resume', 'cover_letter']
    
    def create(self, validated_data):
        applicant_email = self.context['request'].data.get('applicant_email')
        
        if not applicant_email:
            raise serializers.ValidationError("Applicant email is required.")

        return Application.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Updates an application instance. If the 'cover_letter' or 'resume' keys are
        not present in the validated data, the existing values are used.
        """
        instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
        instance.resume = validated_data.get('resume', instance.resume)
        instance.save()
        return instance
