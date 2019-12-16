# -*- coding: utf-8 -*-
from django.http import JsonResponse
from sparrow_cloud.utils.validation_acl import validation_acl
from sparrow_cloud.middleware.base.base_middleware import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)


class ACLMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        ACL VALIDATED
        :param request:
        :return:
        """
        remote_user = request.META.get('REMOTE_USER', None)
        acl_token = request.GET.get('acl_token', None)
        if not acl_token:
            return
        validated, payload = validation_acl(acl_token)
        if not remote_user and acl_token and validated:
            request.META['REMOTE_USER'] = acl_token
            request.META['payload'] = payload
            return
        if remote_user and acl_token and validated:
            return
        if remote_user and validated is False:
            return JsonResponse({"message": "ACL验证未通过"}, status=403)
        if not remote_user and validated is False:
            return JsonResponse({"message": "ACL验证未通过"}, status=403)
