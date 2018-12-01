import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommentService, Comment } from '../comment.service';
import { User } from '../user.service';

@Component({
  selector: 'app-comment',
  templateUrl: './comment.component.html',
  styleUrls: ['./comment.component.scss'],
})
export class CommentComponent {
  @Input() comment: Comment;
  @Input() currentUser: User;
  @Output() delete = new EventEmitter<number>();
  editing = false;
  newCommentText = '';

  constructor(private commentService: CommentService) { }

  startEdit() {
    this.newCommentText = this.comment.text;
    this.editing = true;
  }

  commitEdit() {
    this.commentService.editComment(this.comment.id, this.newCommentText)
      .subscribe(() => {
        this.comment.text = this.newCommentText;
        this.editing = false;
      });
  }

  cancelEdit() {
    this.editing = false;
  }

  doDelete() {
    if (confirm('Are you sure you want to delete this comment?')) {
      this.commentService.deleteComment(this.comment.id).subscribe(() => {
        this.delete.emit(this.comment.id);
      });
    }
  }

}
