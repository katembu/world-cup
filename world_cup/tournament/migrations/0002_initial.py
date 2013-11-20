# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Countries'
        db.create_table(u'tournament_countries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
            ('final_position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'tournament', ['Countries'])

        # Adding model 'GroupPredictions'
        db.create_table(u'tournament_grouppredictions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Countries'])),
            ('position', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'tournament', ['GroupPredictions'])

        # Adding model 'Matches'
        db.create_table(u'tournament_matches', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team', null=True, to=orm['tournament.Countries'])),
            ('home_score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team', null=True, to=orm['tournament.Countries'])),
            ('away_score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner', null=True, to=orm['tournament.Countries'])),
            ('round', self.gf('django.db.models.fields.IntegerField')()),
            ('match_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'tournament', ['Matches'])

        # Adding model 'MatchPredictions'
        db.create_table(u'tournament_matchpredictions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team_coice', null=True, to=orm['tournament.Countries'])),
            ('home_score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team_choice', null=True, to=orm['tournament.Countries'])),
            ('away_score', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('winner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='winner_choice', null=True, to=orm['tournament.Countries'])),
            ('round', self.gf('django.db.models.fields.IntegerField')()),
            ('match_number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'tournament', ['MatchPredictions'])


    def backwards(self, orm):
        # Deleting model 'Countries'
        db.delete_table(u'tournament_countries')

        # Deleting model 'GroupPredictions'
        db.delete_table(u'tournament_grouppredictions')

        # Deleting model 'Matches'
        db.delete_table(u'tournament_matches')

        # Deleting model 'MatchPredictions'
        db.delete_table(u'tournament_matchpredictions')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'tournament.countries': {
            'Meta': {'object_name': 'Countries'},
            'final_position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {})
        },
        u'tournament.grouppredictions': {
            'Meta': {'object_name': 'GroupPredictions'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tournament.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'tournament.matches': {
            'Meta': {'object_name': 'Matches'},
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
            'home_score': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team_coice'", 'null': 'True', 'to': u"orm['tournament.Countries']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_number': ('django.db.models.fields.IntegerField', [], {}),
            'round': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'winner_choice'", 'null': 'True', 'to': u"orm['tournament.Countries']"})
        }
    }

    complete_apps = ['tournament']