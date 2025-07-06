import random
import typing as t

from app.models import Category, Report, StatusReport, Tag, TypeReport
from django.core.management.base import BaseCommand

CATEGORIES = [
    'Infrastructure',
    'Health & Safety',
    'Environmental Issues',
    'Technical Error',
    'Security',
    'Finance & Budget',
    'Logistics',
    'Personnel',
    'Public Relations',
    'Customer Feedback',
    'Legal',
    'Compliance',
    'Emergency',
    'Maintenance',
    'IT & Systems',
]

TAGS = [
    'Urgent',
    'Follow-up',
    'Resolved',
    'Pending',
    'Critical',
    'Internal',
    'External',
    'High Risk',
    'Low Priority',
    'Investigation',
    'Audit',
    'Documentation',
    'System Alert',
    'Manual Check',
    'Recurring Issue',
    'Needs Review',
    'Compliance Required',
    'Delayed',
    'Approved',
    'Rejected',
    'Waiting Response',
    'In Progress',
    'Temporary Fix',
    'Permanent Fix',
    'Training Needed',
    'Third-party',
    'Policy Breach',
    'Data Loss',
    'Scheduled',
    'Out of Scope',
]


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--obj',
            type=int,
            default=100,
            help='Number of report objects to create',
        )

    def _write(self, message: str) -> None:
        self.stdout.write(message)

    def handle(self, *args: t.Any, **options: t.Any) -> None:
        obj_num = options['obj']
        self._write('Starting upload data')
        self.upload_data(obj_num)
        self._write('Data has been uploaded successfully')

    def create_categories(self) -> list[Category]:
        categories = [Category(name=name) for name in CATEGORIES]
        Category.objects.bulk_create(categories)

        assert len(categories) == len(CATEGORIES)
        return categories

    def create_tags(self) -> list[Tag]:
        tags = [Tag(name=name) for name in TAGS]
        Tag.objects.bulk_create(tags)

        assert len(tags) == len(TAGS)
        return tags

    def set_tags_to_report(self, tags: list[Tag]):
        report_tag = Report.tag.through
        _tags = []

        for item in Report.objects.only('id'):
            select_tags = random.sample(tags, k=random.randint(1, 9))
            for tag in select_tags:
                _tags.append(report_tag(report_id=item.id, tag_id=tag.id))

        report_tag.objects.bulk_create(_tags)

        return _tags

    def create_reports(
        self, categories: list[Category], tags: list[Tag], obj_num: int
    ) -> list[Report]:
        reports = []
        for num, item in enumerate(range(1, obj_num + 1), start=1):
            report = Report(
                report_num=num,
                type_report=random.choice(
                    [choice[0] for choice in TypeReport.choices]
                ),
                priority=random.randint(1, 3),
                category=random.choice(categories),
                name=f'Raport name №{num}',
                status_report=random.choice([s.name for s in StatusReport]),
                description=f'Report Description №{num}',
            )
            reports.append(report)

        Report.objects.bulk_create(reports)

        return reports

    def upload_data(self, obj_num: int):
        self._write('Starting upload --- CATEGORIES ---')
        categories = self.create_categories()
        self._write('Category items count: %s' % len(categories))

        self._write('Starting upload --- TAGS ---')
        tags = self.create_tags()
        self._write('Tag items count: %s' % len(tags))

        self._write('Starting upload --- REPORTS ---')
        reports = self.create_reports(
            categories=categories, tags=tags, obj_num=obj_num
        )
        self._write('Reports items count: %s' % len(reports))

        self._write('Starting set --- TAGS --- to --- REPORT ---')
        set_tags = self.set_tags_to_report(tags=tags)
        self._write('Set Tags items count: %s' % len(set_tags))
