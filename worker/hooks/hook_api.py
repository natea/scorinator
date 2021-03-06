import json
import requests
import logging

from api import AUTH, API_URL, get_score_attribute


logger = logging.getLogger('worker')


def send_score(score_attrib_id, project_score_id, value):
    """ Send the score to the API"""
    value = json.dumps(value)
    payload = {
        "score_attribute": score_attrib_id,
        "project_score": project_score_id,
        "score_value": None,
        "result": value,
    }
    r = requests.post("{0}project-score-attributes/".format(API_URL),
                      data=payload, auth=AUTH)
    logger.info(r.json())
    return r.json()


def run(project, result):
    """ given a result, call the api with the results"""
    project_score_id = project.get('project_score_id', None)
    if not project_score_id:
        logger.debug("No project_score_id :(")
        return
    score_attrib_slug = result.get('name', None)
    score_attrib = get_score_attribute(score_attrib_slug)
    score_attrib_id = score_attrib.get('id', None)
    value = result.get('value', None)

    if score_attrib_id and project_score_id and value:
        res = send_score(score_attrib_id, project_score_id, value)
        result['project_score_attribute_id'] = res.get('id')
    else:
        logger.debug("Skip")
    logger.debug("Done")
    return result
