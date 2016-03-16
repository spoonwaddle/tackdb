from tackdb.sessions import db_session


def assert_sessions_equal(seq1, seq2):
    for out1, out2 in zip(seq1, seq2):
        assert out1 == out2


def test_e2e_sequence_1():
    sessions = [
        
        [("BEGIN", None),
         ("SET a 10", None),
         ("GET a", "10"),
         ("BEGIN", None),
         ("SET a 20", None),
         ("GET a", "20"),
         ("ROLLBACK", None),
         ("GET a", "10"),
         ("ROLLBACK", None),
         ("GET a", "NULL"),
         ("END", "NULL")],
        
        [("BEGIN", None),
         ("SET a 30", None),
         ("BEGIN", None),
         ("SET a 40", None),
         ("COMMIT", None),
         ("GET a", "40"),
         ("ROLLBACK", "NO TRANSACTION"),
         ("END", None)],

       [("SET a 50", None),
        ("BEGIN", None),
        ("GET a", "50"),
        ("SET a 60", None),
        ("BEGIN", None),
        ("UNSET a", None),
        ("GET a", "NULL"),
        ("ROLLBACK", None),
        ("GET a", "60"),
        ("COMMIT", None),
        ("GET a", "60"),
        ("END", None)],

       [("SET a 10", None),
        ("BEGIN", None),
        ("NUMEQUALTO 10", '1'),
        ("BEGIN", None),
        ("UNSET a", None),
        ("NUMEQUALTO 10", '0'),
        ("ROLLBACK", None),
        ("NUMEQUALTO 10", '1'),
        ("COMMIT", None),
        ("END", None)]
    ]
    for s in sessions: 
        commands, expected = zip(*s)
        assert_sessions_equal(db_session(commands), expected)
