"""
GitHub Actions 통합 테스트
"""
import os
import sys


def test_github_actions_environment():
    """GitHub Actions 환경 변수 테스트"""
    # 기본적인 환경 테스트
    assert sys.version_info >= (3, 8), "Python 3.8 이상이 필요합니다"
    

def test_project_structure():
    """프로젝트 구조 테스트"""
    # 필수 디렉토리 존재 확인
    assert os.path.exists("backend"), "backend 디렉토리가 존재해야 합니다"
    assert os.path.exists("frontend"), "frontend 디렉토리가 존재해야 합니다"
    assert os.path.exists(".github"), ".github 디렉토리가 존재해야 합니다"
    

def test_github_workflows():
    """GitHub Workflows 파일 존재 테스트"""
    workflows_dir = ".github/workflows"
    assert os.path.exists(workflows_dir), "workflows 디렉토리가 존재해야 합니다"
    
    # 필수 워크플로우 파일들 확인
    required_workflows = [
        "test.yml",
        "pr-comment.yml", 
        "pr-assignee.yml",
        "pr-labeler.yml",
        "pr-code-review.yml",
        "issue-comment.yml",
        "issue-assignee.yml",
        "issue-labeler.yml"
    ]
    
    for workflow in required_workflows:
        workflow_path = os.path.join(workflows_dir, workflow)
        assert os.path.exists(workflow_path), f"{workflow} 파일이 존재해야 합니다"


def test_github_templates():
    """GitHub 템플릿 파일 존재 테스트"""
    # 이슈 템플릿 확인
    assert os.path.exists(".github/ISSUE_TEMPLATE/bug_report.md"), "버그 리포트 템플릿이 존재해야 합니다"
    assert os.path.exists(".github/ISSUE_TEMPLATE/feature_request.md"), "기능 요청 템플릿이 존재해야 합니다"
    
    # PR 템플릿 확인
    assert os.path.exists(".github/PULL_REQUEST_TEMPLATE.md"), "PR 템플릿이 존재해야 합니다"
    
    # CODEOWNERS 파일 확인
    assert os.path.exists(".github/CODEOWNERS"), "CODEOWNERS 파일이 존재해야 합니다"


def test_requirements_file():
    """requirements.txt 파일 테스트"""
    assert os.path.exists("requirements.txt"), "requirements.txt 파일이 존재해야 합니다"
    
    with open("requirements.txt", "r") as f:
        content = f.read()
        assert len(content.strip()) > 0, "requirements.txt 파일이 비어있지 않아야 합니다"


def test_basic_math():
    """기본적인 수학 연산 테스트 (GitHub Actions 동작 확인용)"""
    assert 2 + 2 == 4
    assert 10 - 5 == 5
    assert 3 * 4 == 12
    assert 8 / 2 == 4


def test_string_operations():
    """문자열 연산 테스트"""
    test_string = "GitHub Actions Test"
    assert "GitHub" in test_string
    assert test_string.upper() == "GITHUB ACTIONS TEST"
    assert len(test_string) == 19


def test_list_operations():
    """리스트 연산 테스트"""
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5
    assert sum(test_list) == 15
    assert max(test_list) == 5
    assert min(test_list) == 1


def run_tests():
    """모든 테스트 실행"""
    tests = [
        test_github_actions_environment,
        test_project_structure,
        test_github_workflows,
        test_github_templates,
        test_requirements_file,
        test_basic_math,
        test_string_operations,
        test_list_operations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✅ {test.__name__}: PASSED")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"💥 {test.__name__}: ERROR - {e}")
            failed += 1
    
    print(f"\n📊 테스트 결과: {passed} 통과, {failed} 실패")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 