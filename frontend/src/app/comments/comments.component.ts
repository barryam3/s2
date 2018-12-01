import { Component, Input } from '@angular/core';
import { Song } from '../song.service';
import { CommentService } from '../comment.service';
import { filterInPlace } from '../../utils';
import { User } from '../user.service';

@Component({
  selector: 'app-comments',
  templateUrl: './comments.component.html',
  styleUrls: ['./comments.component.scss'],
})
export class CommentsComponent {
  @Input() song: Song;
  @Input() currentUser: User;

  newCommentText = '';

  constructor(private commentService: CommentService) { }

  onCommentDelete(commentID: number) {
    filterInPlace(this.song.comments, comment => comment.id !== commentID);
  }

  addComment() {
    this.commentService.addComment(this.song.id, this.newCommentText)
      .subscribe(comment => {
        this.song.comments.push(comment);
        this.newCommentText = '';
      });
  }

}
