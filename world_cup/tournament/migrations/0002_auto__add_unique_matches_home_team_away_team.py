# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Matches', fields ['home_team', 'away_team']
        db.create_unique(u'tournament_matches', ['home_team_id', 'away_team_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Matches', fields ['home_team', 'away_team']
        db.delete_unique(u'tournament_matches', ['home_team_id', 'away_team_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tournament.brackets': {
            'Meta': {'object_name': 'Brackets'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_management.CustomUser']"})
        },
        u'tournament.competitivegroups': {
            'Meta': {'object_name': 'CompetitiveGroups'},
            'brackets': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['tournament.Brackets']", 'symmetrical': 'False'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_management.CustomUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'tournament.countries': {
            'Meta': {'object_name': 'Countries'},
            'final_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'world_rank': ('django.db.models.fields.IntegerField', [], {'default': '99', 'null': 'True', 'blank': 'True'})
        },
        u'tournament.grouppermissions': {
            'Meta': {'object_name': 'GroupPermissions'},
            'allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournament.CompetitiveGroups']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['user_management.CustomUser']", 'null': 'True'})
        },
        u'tournament.grouppredictions': {
            'Meta': {'object_name': 'GroupPredictions'},
            'bracket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournament.Brackets']"}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournament.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        u'tournament.matches': {
            'Meta': {'unique_together': "(('home_team', 'away_team'),)", 'object_name': 'Matches'},
            'away_score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'null': 'True', 'to': u"orm['tournament.Countries']"}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'null': 'True', 'to': u"orm['tournament.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_number': ('django.db.models.fields.IntegerField', [], {}),
            'round': ('django.db.models.fields.IntegerField', [], {}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner'", 'null': 'True', 'to': u"orm['tournament.Countries']"})
        },
        u'tournament.matchpredictions': {
            'Meta': {'object_name': 'MatchPredictions'},
            'away_score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team_choice'", 'null': 'True', 'to': u"orm['tournament.Countries']"}),
            'bracket': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournament.Brackets']"}),
            'home_score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team_coice'", 'null': 'True', 'to': u"orm['tournament.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_number': ('django.db.models.fields.IntegerField', [], {}),
            'round': ('django.db.models.fields.IntegerField', [], {}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner_choice'", 'null': 'True', 'to': u"orm['tournament.Countries']"})
        },
        u'user_management.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'message_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_full_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['tournament']