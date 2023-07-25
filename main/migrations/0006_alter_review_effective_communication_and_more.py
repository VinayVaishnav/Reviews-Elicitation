# Generated by Django 4.2.2 on 2023-07-25 16:02

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_review_ethical_professionalism_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='Effective_Communication',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Team Player', 'Team Player'), ('Cooperative Collaborator', 'Cooperative Collaborator'), ('Supportive Teammate', 'Supportive Teammate'), ('Independent Worker', 'Independent Worker'), ('Relationship Builder', 'Relationship Builder'), ('Self-Reliant', 'Self-Reliant'), ('Friendly Service Provider', 'Friendly Service Provider'), ('Empathetic Listener', 'Empathetic Listener'), ('Culturally Neutral', 'Culturally Neutral'), ('Customer-Focused Problem-Solver', 'Customer-Focused Problem-Solver'), ('Approachable and Friendly', 'Approachable and Friendly'), ('Individual Contributor', 'Individual Contributor'), ('Empowering Coach', 'Empowering Coach'), ('Results-Focused Educator', 'Results-Focused Educator'), ('Effective Teacher', 'Effective Teacher')], max_length=355),
        ),
        migrations.AlterField(
            model_name='review',
            name='Ethical_Professionalism',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Reliable and Trustworthy', 'Reliable and Trustworthy'), ('Honest Communicator', 'Honest Communicator'), ('Sincere and Transparent', 'Sincere and Transparent'), ('Genuine and Authentic', 'Genuine and Authentic'), ('Respectful of Diversity', 'Respectful of Diversity'), ('Confident and Self-Assured', 'Confident and Self-Assured'), ('Hardworking and Dedicated', 'Hardworking and Dedicated'), ('Endurance', 'Endurance'), ('Detail-Oriented', 'Detail-Oriented'), ('Organized and Systematic', 'Organized and Systematic'), ('Ambitious and Aspiring', 'Ambitious and Aspiring'), ('Consistent but Moderate Performance', 'Consistent but Moderate Performance'), ('Patiently Ambitious', 'Patiently Ambitious'), ('Continuous Learner', 'Continuous Learner'), ('Pursuer of Excellence', 'Pursuer of Excellence')], max_length=355),
        ),
        migrations.AlterField(
            model_name='review',
            name='Responsible_Leadership',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Responsible Leader', 'Responsible Leader'), ('Responsible Delegator', 'Responsible Delegator'), ('Takes Ownership', 'Takes Ownership'), ('Engaging Team Manager', 'Engaging Team Manager'), ('People Person', 'People Person'), ('Inspirational Communicator', 'Inspirational Communicator'), ('Extraverted Networker', 'Extraverted Networker'), ('Visionary Thinker', 'Visionary Thinker'), ('Strategic Planner', 'Strategic Planner'), ('Future-Oriented', 'Future-Oriented'), ('Setting Realistic Goals', 'Setting Realistic Goals'), ('Self-Disciplined Professional', 'Self-Disciplined Professional'), ('Calm under Pressure', 'Calm under Pressure'), ('Self-Motivated', 'Self-Motivated'), ('Maintains Composure', 'Maintains Composure')], max_length=355),
        ),
        migrations.AlterField(
            model_name='review',
            name='Thinking_and_Problem_Solving',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Logical Problem Solver', 'Logical Problem Solver'), ('Systematic Decision Maker', 'Systematic Decision Maker'), ('Decisive Thinker', 'Decisive Thinker'), ('Cautious Evaluator', 'Cautious Evaluator'), ('Learning Oriented', 'Learning Oriented'), ('Quick Learner', 'Quick Learner'), ('Slow Learner', 'Slow Learner'), ('Sound Reasoner', 'Sound Reasoner'), ('Curious Explorer', 'Curious Explorer'), ('Outside-the-Box Thinker', 'Outside-the-Box Thinker'), ('Innovative and Original', 'Innovative and Original'), ('Careful and Reasoned', 'Careful and Reasoned'), ('Embraces Feedback', 'Embraces Feedback'), ('Accepts Constructive Criticism', 'Accepts Constructive Criticism'), ('Adaptable Team Player', 'Adaptable Team Player')], max_length=355),
        ),
    ]
