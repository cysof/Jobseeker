from rest_framework import serializers
from .models import Company, Job, JobSkill, Skill, CustomUser, Application

# Company serializer
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'description', 'website', 'company_logo']

# Job serializer
class JobSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(queryset=Company.objects.all(), slug_field='name')

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'company', 'location', 'job_type', 'experience_level', 'salary', 'is_active']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']
        

# JobSkill serializer
class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = ['id', 'job', 'skills']  # Ensure both 'job' and 'skills' are included here.

    def create(self, validated_data):
        job = validated_data.get('job')  # Ensure job is extracted from validated data.
        skills = validated_data.get('skills')  # Ensure skills are extracted.
        
        if not job:
            raise serializers.ValidationError({"job": "This field is required."})
        
        if not skills:
            raise serializers.ValidationError({"skills": "This field is required."})

        job_skill = JobSkill.objects.create(job=job, skills=skills)
        return job_skill

        


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
    job = serializers.StringRelatedField(read_only=True)  # Display string representation of job
    company = serializers.StringRelatedField(read_only=True)  # Display string representation of company
    
    job_id = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), write_only=True)  # Accept job_id for creation
    company_id = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), write_only=True)  # Accept company_id for creation

    class Meta:
        model = Application
        fields = ['id', 'job', 'company', 'job_id', 'company_id', 'applicant_name', 'applicant_email', 'resume', 'cover_letter']

    def create(self, validated_data):
        # Extract the foreign keys from validated_data
        job = validated_data.pop('job_id')  # Extract job_id
        company = validated_data.pop('company_id')  # Extract company_id
        
        # Create the application instance with the job and company IDs
        application = Application.objects.create(job=job, company=company, **validated_data)
        return application

    def update(self, instance, validated_data):
        """
        Updates an application instance. If the 'cover_letter' or 'resume' keys are
        not present in the validated data, the existing values are used.
        """
        instance.cover_letter = validated_data.get('cover_letter', instance.cover_letter)
        instance.resume = validated_data.get('resume', instance.resume)
        instance.save()
        return instance