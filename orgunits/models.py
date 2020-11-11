"""
Copyright 2020 ООО «Верме»
"""

from django.db import models
from django.db.models.expressions import RawSQL


class OrganizationQuerySet(models.QuerySet):
    def tree_downwards(self, root_org_id):
        """
        Возвращает корневую организацию с запрашиваемым root_org_id и всех её детей любого уровня вложенности

        :type root_org_id: int
        """
        query = '''
        WITH RECURSIVE cte AS (
        SELECT o.id,o.name,o.code,o.parent_id FROM orgunits_organization o WHERE id=%s
        UNION ALL 
        SELECT o.id,o.name,o.code,o.parent_id 
        FROM orgunits_organization o JOIN cte c ON o.parent_id=c.id) SELECT id FROM cte
        '''
        return self.filter(pk__in=RawSQL(query, [root_org_id]))


    def tree_upwards(self, child_org_id):
        """
        Возвращает корневую организацию с запрашиваемым child_org_id и всех её родителей любого уровня вложенности

        :type child_org_id: int
        """
        query = '''
        WITH RECURSIVE cte AS (
        SELECT o.id,o.name,o.code,o.parent_id FROM orgunits_organization o WHERE id=%s
        UNION ALL
        SELECT o.id,o.name,o.code,o.parent_id
        FROM orgunits_organization o JOIN cte c ON o.id=c.parent_id) SELECT id FROM cte
        '''
        return self.filter(pk__in=RawSQL(query, [child_org_id]))


class Organization(models.Model):
    """ Организация """

    objects = OrganizationQuerySet.as_manager()

    name = models.CharField(max_length=1000, blank=False, null=False, verbose_name="Название")
    code = models.CharField(max_length=1000, blank=False, null=False, unique=True, verbose_name="Код")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT, verbose_name="Вышестоящая организация",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Организация"
        verbose_name = "Организации"

    def __str__(self):
        return self.name

    def parents(self):
        """
        Возвращает всех родителей любого уровня вложенности

        :rtype: django.db.models.QuerySet
        """
        return Organization.objects.tree_upwards(self.id).exclude(pk=self.id)

    def children(self):
        """
        Возвращает всех детей любого уровня вложенности

        :rtype: django.db.models.QuerySet
        """
        return Organization.objects.tree_downwards(self.id).exclude(pk=self.id)
