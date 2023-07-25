# Generated by Django 4.2.1 on 2023-07-25 07:34

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_communication_review_effective_communication_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='Effective_Communication',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Team Player'), (2, 'Cooperative Collaborator'), (3, 'Supportive Teammate'), (4, 'Independent Worker'), (5, 'Relationship Builder'), (6, 'Self-Reliant'), (7, 'Friendly Service Provider'), (8, 'Empathetic Listener'), (9, 'Culturally Neutral'), (10, 'Customer-Focused Problem-Solver'), (11, 'Approachable and Friendly'), (12, 'Individual Contributor'), (13, 'Empowering Coach'), (14, 'Results-Focused Educator'), (15, 'Effective Teacher')], max_length=255),
        ),
        migrations.AlterField(
            model_name='review',
            name='Ethical_Professionalism',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Reliable and Trustworthy'), (2, 'Honest Communicator'), (3, 'Sincere and Transparent'), (4, 'Genuine and Authentic'), (5, 'Respectful of Diversity'), (6, 'Confident and Self-Assured'), (7, 'Hardworking and Dedicated'), (8, 'Endurance'), (9, 'Detail-Oriented'), (10, 'Organized and Systematic'), (11, 'Ambitious and Aspiring'), (12, 'Consistent but Moderate Performance'), (13, 'Patiently Ambitious'), (14, 'Continuous Learner'), (15, 'Pursuer of Excellence')], max_length=255),
        ),
        migrations.AlterField(
            model_name='review',
            name='Responsible_Leadership',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Responsible Leader'), (2, 'Responsible Delegator'), (3, 'Takes Ownership'), (4, 'Engaging Team Manager'), (5, 'People Person'), (6, 'Inspirational Communicator'), (7, 'Extraverted Networker'), (8, 'Visionary Thinker'), (9, 'Strategic Planner'), (10, 'Future-Oriented'), (11, 'Setting Realistic Goals'), (12, 'Self-Disciplined Professional'), (13, 'Calm under Pressure'), (14, 'Self-Motivated'), (15, 'Maintains Composure')], max_length=255),
        ),
        migrations.AlterField(
            model_name='review',
            name='Thinking_and_Problem_Solving',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Logical Problem Solver'), (2, 'Systematic Decision Maker'), (3, 'Decisive Thinker'), (4, 'Cautious Evaluator'), (5, 'Learning Oriented'), (6, 'Quick Learner'), (7, 'Slow Learner'), (8, 'Sound Reasoner'), (9, 'Curious Explorer'), (10, 'Outside-the-Box Thinker'), (11, 'Innovative and Original'), (12, 'Careful and Reasoned'), (13, 'Embraces Feedback'), (14, 'Accepts Constructive Criticism'), (15, 'Adaptable Team Player')], max_length=255),
        ),
    ]
