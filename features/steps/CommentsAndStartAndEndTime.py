from behave import *
from time import gmtime, strftime
# import meterage

# WHENS

@when(u'the user adds a new entry to log with an unspecified start time')
def step_impl(context):
    context.rv = context.app.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here',
        start_time='',
        end_time='<17:30>'
    ), follow_redirects=True)


@when(u'click the entry, the user would be able to add a comment each time')
def step_impl(context):
    context.rv = context.app.post('/1/add_comments', data=dict(
        comment_input='<FinalVERSION>'
    ), follow_redirects=True)


@when(u'the user presses end_task')
def step_impl(context):
    context.rv = context.app.post('/1/add_end_time', follow_redirects=True)


# THENS

@then(u'the comment should appear right after added')
def step_impl(context):
    assert '&lt;FinalVERSION&gt;' in context.rv.get_data()


@then(u'the username should displayed right next to the comment')
def step_impl(context):
    assert 'by hari' in context.rv.get_data()


@then(u'start time will auto sign')
def step_impl(context):
    assert strftime("%Y-%m-%d %H:%M", gmtime()) in context.rv.get_data(), context.rv.get_data()


@then(u'end time will auto sign')
def step_impl(context):
    assert 'End at: '+ strftime("%Y-%m-%d %H:%M", gmtime()) in context.rv.get_data()